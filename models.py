from flask_sqlalchemy import SQLAlchemy

# Do not initialize db here, leave it to app.py
db = SQLAlchemy()

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)  # Indexed for fast searching
    description = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(50), nullable=False, index=True)  # Indexed for faster search on 'type'
    price = db.Column(db.String(100), nullable=True)
    contact_name = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    duration_days = db.Column(db.Integer, nullable=True)
    duration_nights = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Package {self.name}>"

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)  # Indexed for fast searching
    description = db.Column(db.String(255))
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    image = db.Column(db.String(255))

    def __repr__(self):
        return f'<Service {self.name}>'

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    testimonial_text = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)  # Indexed for faster search
    location = db.Column(db.String(100), nullable=False, index=True)  # Indexed for faster search by location
    rating = db.Column(db.Integer, nullable=False)  # Indexed for faster sorting/search by rating
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Testimonial {self.name} - {self.location}>"

class TeamMembers(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)  # Indexed for faster search by name
    position = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    is_head = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f"<TeamMember(name={self.name}, position={self.position}, is_head={self.is_head})>"