import json
from datetime import date
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from sqlalchemy import func
import config
from models import db, User, Sprint, Asset, Stream, IncomeEntry, AIContent, Goal
from meo import ai

login_manager = LoginManager()

TIER_RANK = {"lifetime": 1, "starter": 2, "pro": 3, "studio": 4}


def tier_required(min_tier):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if TIER_RANK.get(current_user.tier, 0) < TIER_RANK.get(min_tier, 0):
                flash("Upgrade your plan to access this feature.", "error")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return decorated
    return decorator


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = config.SECRET_KEY
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _income_summary(user_id):
    today_str = date.today().isoformat()
    month_str = today_str[:7]

    def q():
        return (db.session.query(func.coalesce(func.sum(IncomeEntry.amount_gbp), 0))
                .join(Asset).filter(Asset.user_id == user_id))

    today_total = q().filter(IncomeEntry.earned_date == today_str).scalar()
    month_total = q().filter(IncomeEntry.earned_date.like(f"{month_str}%")).scalar()
    all_time    = q().scalar()

    by_stream_rows = (
        db.session.query(IncomeEntry.stream_type,
                         func.sum(IncomeEntry.amount_gbp).label("total"))
        .join(Asset).filter(Asset.user_id == user_id)
        .group_by(IncomeEntry.stream_type).all()
    )
    by_stream = {r.stream_type: round(r.total, 2) for r in by_stream_rows if r.stream_type}

    by_asset_rows = (
        db.session.query(Asset.name, func.sum(IncomeEntry.amount_gbp).label("total"))
        .join(IncomeEntry).filter(Asset.user_id == user_id)
        .group_by(Asset.id, Asset.name)
        .order_by(func.sum(IncomeEntry.amount_gbp).desc())
        .all()
    )
    by_asset = [{"name": r.name, "total": round(r.total, 2)} for r in by_asset_rows]

    return {
        "today":      round(today_total, 2),
        "this_month": round(month_total, 2),
        "all_time":   round(all_time, 2),
        "by_stream":  by_stream,
        "by_asset":   by_asset,
    }


def _active_goal(user_id):
    g = Goal.query.filter_by(active=True, user_id=user_id).order_by(Goal.start_date.desc()).first()
    if not g:
        return None
    earned = (db.session.query(func.coalesce(func.sum(IncomeEntry.amount_gbp), 0))
              .join(Asset).filter(
                  Asset.user_id == user_id,
                  IncomeEntry.earned_date >= g.start_date,
                  IncomeEntry.earned_date <= g.end_date,
              ).scalar())
    gap = max(g.target_gbp - earned, 0)
    pct = min(earned / g.target_gbp * 100, 100) if g.target_gbp else 0
    return {
        "id":         g.id,
        "label":      g.label,
        "target_gbp": g.target_gbp,
        "earned_gbp": round(earned, 2),
        "gap_gbp":    round(gap, 2),
        "pct":        round(pct, 1),
        "start_date": g.start_date,
        "end_date":   g.end_date,
    }


@app.context_processor
def inject_globals():
    if current_user.is_authenticated:
        return dict(goal=_active_goal(current_user.id), current_user=current_user)
    return dict(goal=None, current_user=current_user)


# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email    = request.form["email"].strip().lower()
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "error")
            return redirect(url_for("signup"))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("auth/signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email    = request.form["email"].strip().lower()
        password = request.form["password"]
        user     = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(request.args.get("next") or url_for("dashboard"))
    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")


@app.route("/dashboard")
@login_required
def dashboard():
    summary = _income_summary(current_user.id)
    return render_template("index.html", summary=summary, today=date.today())


@app.route("/goal", methods=["POST"])
@login_required
def set_goal():
    Goal.query.filter_by(active=True, user_id=current_user.id).update({"active": False})
    db.session.add(Goal(
        user_id=current_user.id,
        label=request.form["label"],
        target_gbp=float(request.form["target_gbp"]),
        start_date=request.form["start_date"],
        end_date=request.form["end_date"],
    ))
    db.session.commit()
    return redirect(url_for("dashboard"))


# ── Assets ────────────────────────────────────────────────────────────────────

@app.route("/assets")
@login_required
@tier_required("starter")
def assets():
    all_assets = Asset.query.filter_by(user_id=current_user.id).order_by(Asset.created_at.desc()).all()
    return render_template("assets.html", assets=all_assets)


@app.route("/assets", methods=["POST"])
@login_required
@tier_required("starter")
def create_asset():
    db.session.add(Asset(
        user_id=current_user.id,
        name=request.form["name"],
        description=request.form.get("description", ""),
        type=request.form.get("type", "tool"),
        complexity_tier=request.form.get("complexity_tier", "quick-win"),
        tech_stack=request.form.get("tech_stack", ""),
        time_invested_hours=float(request.form.get("time_invested_hours") or 0),
    ))
    db.session.commit()
    flash("Asset created.", "success")
    return redirect(url_for("assets"))


@app.route("/assets/<int:asset_id>", methods=["POST"])
@login_required
@tier_required("starter")
def update_asset(asset_id):
    a = Asset.query.filter_by(id=asset_id, user_id=current_user.id).first_or_404()
    if request.form.get("add_hours"):
        a.time_invested_hours = (a.time_invested_hours or 0) + float(request.form["add_hours"])
    else:
        a.status = request.form.get("status", a.status)
        if request.form.get("time_invested_hours"):
            a.time_invested_hours = float(request.form["time_invested_hours"])
    db.session.commit()
    return redirect(url_for("assets"))


@app.route("/assets/<int:asset_id>/streams", methods=["POST"])
@login_required
@tier_required("starter")
def add_stream(asset_id):
    Asset.query.filter_by(id=asset_id, user_id=current_user.id).first_or_404()
    db.session.add(Stream(
        asset_id=asset_id,
        stream_type=request.form["stream_type"],
        platform=request.form.get("platform", ""),
        url=request.form.get("url", ""),
        price_min=float(request.form["price_min"]) if request.form.get("price_min") else None,
        price_max=float(request.form["price_max"]) if request.form.get("price_max") else None,
    ))
    db.session.commit()
    flash("Stream added.", "success")
    return redirect(url_for("assets"))


# ── Sprint Board ──────────────────────────────────────────────────────────────

@app.route("/sprint")
@login_required
@tier_required("starter")
def sprint_board():
    active     = Sprint.query.filter_by(status="active", user_id=current_user.id).order_by(Sprint.created_at.desc()).first()
    all_assets_for_sprint = Asset.query.filter_by(user_id=current_user.id).order_by(Asset.name).all() if active else []
    all_sprints = Sprint.query.filter_by(user_id=current_user.id).order_by(Sprint.created_at.desc()).all()
    return render_template("sprint.html", sprint=active,
                           all_assets_for_sprint=all_assets_for_sprint,
                           all_sprints=all_sprints)


@app.route("/sprints", methods=["POST"])
@login_required
@tier_required("starter")
def create_sprint():
    db.session.add(Sprint(
        user_id=current_user.id,
        name=request.form["name"],
        type=request.form.get("type", "onboarding"),
        start_date=request.form.get("start_date"),
        end_date=request.form.get("end_date"),
        notes=request.form.get("notes", ""),
    ))
    db.session.commit()
    return redirect(url_for("sprint_board"))


@app.route("/sprints/<int:sprint_id>/update", methods=["POST"])
@login_required
@tier_required("starter")
def update_sprint(sprint_id):
    s = Sprint.query.filter_by(id=sprint_id, user_id=current_user.id).first_or_404()
    s.name       = request.form.get("name", s.name)
    s.type       = request.form.get("type", s.type)
    s.start_date = request.form.get("start_date", s.start_date)
    s.end_date   = request.form.get("end_date", s.end_date)
    s.notes      = request.form.get("notes", s.notes)
    db.session.commit()
    flash("Sprint updated.", "success")
    return redirect(url_for("sprint_board"))


@app.route("/sprints/<int:sprint_id>/complete", methods=["POST"])
@login_required
@tier_required("starter")
def complete_sprint(sprint_id):
    Sprint.query.filter_by(id=sprint_id, user_id=current_user.id).first_or_404().status = "completed"
    db.session.commit()
    flash("Sprint completed. Start a new one below.", "success")
    return redirect(url_for("sprint_board"))


@app.route("/sprints/<int:sprint_id>/assign", methods=["POST"])
@login_required
@tier_required("starter")
def assign_asset(sprint_id):
    Sprint.query.filter_by(id=sprint_id, user_id=current_user.id).first_or_404()
    a = Asset.query.filter_by(id=int(request.form["asset_id"]), user_id=current_user.id).first_or_404()
    a.sprint_id   = sprint_id
    a.sprint_week = int(request.form.get("sprint_week", 1))
    db.session.commit()
    return redirect(url_for("sprint_board"))


# ── Income ────────────────────────────────────────────────────────────────────

@app.route("/income")
@login_required
def income():
    entries = (IncomeEntry.query.join(Asset)
               .filter(Asset.user_id == current_user.id)
               .order_by(IncomeEntry.earned_date.desc()).limit(100).all())
    all_assets = Asset.query.filter_by(user_id=current_user.id).order_by(Asset.name).all()
    summary    = _income_summary(current_user.id)
    return render_template("income.html", entries=entries, assets=all_assets, summary=summary)


@app.route("/income", methods=["POST"])
@login_required
def log_income():
    Asset.query.filter_by(id=int(request.form["asset_id"]), user_id=current_user.id).first_or_404()
    db.session.add(IncomeEntry(
        asset_id=int(request.form["asset_id"]),
        stream_type=request.form.get("stream_type", ""),
        platform=request.form.get("platform", ""),
        amount_gbp=float(request.form["amount_gbp"]),
        earned_date=request.form["earned_date"],
        notes=request.form.get("notes", ""),
    ))
    db.session.commit()
    flash("Income logged.", "success")
    return redirect(url_for("income"))


# ── Gig Generator ─────────────────────────────────────────────────────────────

@app.route("/gig")
@login_required
@tier_required("pro")
def gig():
    all_assets = Asset.query.filter_by(user_id=current_user.id).order_by(Asset.name).all()
    return render_template("gig.html", assets=all_assets, content_types=ai.CONTENT_TYPES)


@app.route("/gig/generate", methods=["POST"])
@login_required
@tier_required("pro")
def generate_gig():
    asset        = Asset.query.filter_by(id=int(request.form["asset_id"]), user_id=current_user.id).first_or_404()
    content_type = request.form["content_type"]
    asset_dict   = {
        "name":                asset.name,
        "description":         asset.description or "",
        "type":                asset.type,
        "complexity_tier":     asset.complexity_tier,
        "tech_stack":          asset.tech_stack or "",
        "time_invested_hours": asset.time_invested_hours,
    }

    try:
        if content_type == "all":
            raw_results = {ct: fn(asset_dict) for ct, fn in ai._GENERATORS.items()}
        else:
            raw_results = {content_type: ai._GENERATORS[content_type](asset_dict)}
    except Exception as e:
        return f'<p class="text-red-600 text-sm p-4">Error: {e}</p>', 500

    for ct, content in raw_results.items():
        existing = AIContent.query.filter_by(asset_id=asset.id, content_type=ct).first()
        if existing:
            existing.content = content
        else:
            db.session.add(AIContent(asset_id=asset.id, content_type=ct, content=content))
    db.session.commit()

    results = {}
    for ct, content in raw_results.items():
        try:
            results[ct] = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            results[ct] = {"raw": content}

    return render_template("partials/gig_result.html", results=results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
