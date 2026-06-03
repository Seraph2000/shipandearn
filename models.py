from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    tier          = db.Column(db.String(20), nullable=False, default="starter")
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    sprints = db.relationship("Sprint", backref="user", lazy=True)
    assets  = db.relationship("Asset",  backref="user", lazy=True)
    goals   = db.relationship("Goal",   backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Sprint(db.Model):
    __tablename__ = "sprints"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name       = db.Column(db.String(200), nullable=False)
    type       = db.Column(db.String(50),  nullable=False, default="onboarding")
    status     = db.Column(db.String(50),  nullable=False, default="active")
    start_date = db.Column(db.String(20))
    end_date   = db.Column(db.String(20))
    notes      = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assets     = db.relationship("Asset", backref="sprint", lazy=True)


class Asset(db.Model):
    __tablename__ = "assets"
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name                = db.Column(db.String(200), nullable=False)
    description         = db.Column(db.Text)
    type                = db.Column(db.String(50),  nullable=False, default="tool")
    complexity_tier     = db.Column(db.String(50),  nullable=False, default="quick-win")
    status              = db.Column(db.String(50),  nullable=False, default="idea")
    tech_stack          = db.Column(db.String(200))
    time_invested_hours = db.Column(db.Float, default=0)
    sprint_id           = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    sprint_week         = db.Column(db.Integer)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)

    streams        = db.relationship("Stream",      backref="asset", lazy=True,
                                     cascade="all, delete-orphan")
    income_entries = db.relationship("IncomeEntry", backref="asset", lazy=True,
                                     cascade="all, delete-orphan")
    ai_content     = db.relationship("AIContent",   backref="asset", lazy=True,
                                     cascade="all, delete-orphan")

    @property
    def total_income(self):
        return round(sum(e.amount_gbp for e in self.income_entries), 2)

    @property
    def streams_by_type(self):
        return {s.stream_type: s for s in self.streams}


class Stream(db.Model):
    __tablename__ = "streams"
    id          = db.Column(db.Integer, primary_key=True)
    asset_id    = db.Column(db.Integer, db.ForeignKey("assets.id", ondelete="CASCADE"),
                            nullable=False)
    stream_type = db.Column(db.String(50),  nullable=False)
    platform    = db.Column(db.String(100))
    url         = db.Column(db.String(500))
    price_min   = db.Column(db.Float)
    price_max   = db.Column(db.Float)
    status      = db.Column(db.String(50), nullable=False, default="draft")
    created_at  = db.Column(db.DateTime,   default=datetime.utcnow)


class IncomeEntry(db.Model):
    __tablename__ = "income_entries"
    id          = db.Column(db.Integer, primary_key=True)
    asset_id    = db.Column(db.Integer, db.ForeignKey("assets.id", ondelete="CASCADE"),
                            nullable=False)
    stream_id   = db.Column(db.Integer, db.ForeignKey("streams.id"))
    stream_type = db.Column(db.String(50))
    platform    = db.Column(db.String(100))
    amount_gbp  = db.Column(db.Float, nullable=False)
    earned_date = db.Column(db.String(20), nullable=False)
    notes       = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class AIContent(db.Model):
    __tablename__ = "ai_content"
    id           = db.Column(db.Integer, primary_key=True)
    asset_id     = db.Column(db.Integer, db.ForeignKey("assets.id", ondelete="CASCADE"),
                             nullable=False)
    content_type = db.Column(db.String(50),  nullable=False)
    content      = db.Column(db.Text, nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("asset_id", "content_type"),)


class Goal(db.Model):
    __tablename__ = "goals"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    label      = db.Column(db.String(100), nullable=False)
    period     = db.Column(db.String(20),  nullable=False, default="monthly")
    target_gbp = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.String(20),  nullable=False)
    end_date   = db.Column(db.String(20),  nullable=False)
    active     = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
