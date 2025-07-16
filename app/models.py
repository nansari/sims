# https://github.com/dr5hn/countries-states-cities-database
# https://flask-sqlalchemy.readthedocs.io/en/stable/
# http://medium.com/@ramanbazhanau/mastering-sqlalchemy-a-comprehensive-guide-for-python-developers-ddb3d9f2e829

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from flask_login import UserMixin
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(user_id):
    """Load user."""
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    """User model."""
    # UserMixin provides - is_authenticated, is_active, is_anonymous, get_id()
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,)
                                            
    password: so.Mapped['Password'] = so.relationship(back_populates='user', cascade='all, delete-orphan')
    bithdate: so.Mapped[int] = so.mapped_column(
        sa.Integer(),
        sa.CheckConstraint('bithdate BETWEEN 1950 and 2099'))
    
    
    @property
    def password_hash(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        """Set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password."""
        if self.password:
            return check_password_hash(self.password.password_hash, password)
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Password(db.Model):
    """Password model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), unique=True)
    user: so.Mapped['User'] = so.relationship(back_populates='password')
    
# class Post(db.Model):
#     """Post model."""
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     body: so.Mapped[str] = so.mapped_column(sa.String(140))
#     timestamp: so.Mapped[datetime] = so.mapped_column(
#         index=True, default=lambda: datetime.now(timezone.utc))
#     user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
#                                                index=True)

#     author: so.Mapped[User] = so.relationship(back_populates='posts')

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

class Role(db.Model):
    """Role model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32), unique=True)

class UserRole(db.Model):
    """User role model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Role.id))


class Regions(db.Model):
    """Represents a region in the world.

    Attributes:
        id (int): The primary key for the region.
        name (str): The name of the region.
        translations (str): Translations of the region name.
        created_at (datetime): The timestamp when the region was created.
        updated_at (datetime): The timestamp when the region was last updated.
        flag (bool): A flag indicating the status of the region.
        wikiDataId (str): The WikiData ID for the region.
    """
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    translations: so.Mapped[str] = so.mapped_column(sa.Text)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    def __repr__(self):
        return f'<Region {self.name}>'


class Subregions(db.Model):
    """Represents a subregion within a region.

    Attributes:
        id (int): The primary key for the subregion.
        name (str): The name of the subregion.
        translations (str): Translations of the subregion name.
        region_id (int): The foreign key for the region this subregion belongs to.
        created_at (datetime): The timestamp when the subregion was created.
        updated_at (datetime): The timestamp when the subregion was last updated.
        flag (bool): A flag indicating the status of the subregion.
        wikiDataId (str): The WikiData ID for the subregion.
        region (Regions): The relationship to the parent region.
    """
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    translations: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('regions.id'), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    region: so.Mapped['Regions'] = so.relationship()

    def __repr__(self):
        return f'<Subregion {self.name}>'


class Countries(db.Model):
    """Represents a country.

    Attributes:
        id (int): The primary key for the country.
        name (str): The name of the country.
        iso3 (str): The 3-letter ISO code for the country.
        numeric_code (str): The numeric code for the country.
        iso2 (str): The 2-letter ISO code for the country.
        phonecode (str): The phone code for the country.
        capital (str): The capital of the country.
        currency (str): The currency of the country.
        currency_name (str): The name of the currency.
        currency_symbol (str): The symbol of the currency.
        tld (str): The top-level domain of the country.
        native (str): The native name of the country.
        region (str): The region of the country.
        region_id (int): The foreign key for the region this country belongs to.
        subregion (str): The subregion of the country.
        subregion_id (int): The foreign key for the subregion this country belongs to.
        nationality (str): The nationality of the country.
        timezones (str): The timezones of the country.
        translations (str): Translations of the country name.
        latitude (float): The latitude of the country.
        longitude (float): The longitude of the country.
        emoji (str): The emoji for the country.
        emojiU (str): The unicode for the country's emoji.
        created_at (datetime): The timestamp when the country was created.
        updated_at (datetime): The timestamp when the country was last updated.
        flag (bool): A flag indicating the status of the country.
        wikiDataId (str): The WikiData ID for the country.
        region_ref (Regions): The relationship to the parent region.
        subregion_ref (Subregions): The relationship to the parent subregion.
    """
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    iso3: so.Mapped[str] = so.mapped_column(sa.String(3), nullable=True)
    numeric_code: so.Mapped[str] = so.mapped_column(sa.String(3), nullable=True)
    iso2: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=True)
    phonecode: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    capital: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    currency: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    currency_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    currency_symbol: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    tld: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    native: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    region: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('regions.id'), nullable=True)
    subregion: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    subregion_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('subregions.id'), nullable=True)
    nationality: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    timezones: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    translations: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(10, 8), nullable=True)
    longitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(11, 8), nullable=True)
    emoji: so.Mapped[str] = so.mapped_column(sa.String(191), nullable=True)
    emojiU: so.Mapped[str] = so.mapped_column(sa.String(191), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    region_ref: so.Mapped['Regions'] = so.relationship(foreign_keys=[region_id])
    subregion_ref: so.Mapped['Subregions'] = so.relationship(foreign_keys=[subregion_id])

    def __repr__(self):
        return f'<Country {self.name}>'


class States(db.Model):
    """Represents a state within a country.

    Attributes:
        id (int): The primary key for the state.
        name (str): The name of the state.
        country_id (int): The foreign key for the country this state belongs to.
        country_code (str): The 2-letter code of the country.
        fips_code (str): The FIPS code for the state.
        iso2 (str): The 2-letter ISO code for the state.
        type (str): The type of the state.
        level (int): The level of the state.
        parent_id (int): The ID of the parent state.
        native (str): The native name of the state.
        latitude (float): The latitude of the state.
        longitude (float): The longitude of the state.
        created_at (datetime): The timestamp when the state was created.
        updated_at (datetime): The timestamp when the state was last updated.
        flag (bool): A flag indicating the status of the state.
        wikiDataId (str): The WikiData ID for the state.
        country (Countries): The relationship to the parent country.
    """
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'), nullable=False)
    country_code: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=False)
    fips_code: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    iso2: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(191), nullable=True)
    level: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    parent_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    native: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(10, 8), nullable=True)
    longitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(11, 8), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    country: so.Mapped['Countries'] = so.relationship()

    def __repr__(self):
        return f'<State {self.name}>'


class Cities(db.Model):
    """Represents a city within a state.

    Attributes:
        id (int): The primary key for the city.
        name (str): The name of the city.
        state_id (int): The foreign key for the state this city belongs to.
        state_code (str): The code of the state.
        country_id (int): The foreign key for the country this city belongs to.
        country_code (str): The 2-letter code of the country.
        latitude (float): The latitude of the city.
        longitude (float): The longitude of the city.
        created_at (datetime): The timestamp when the city was created.
        updated_at (datetime): The timestamp when the city was last updated.
        flag (bool): A flag indicating the status of the city.
        wikiDataId (str): The WikiData ID for the city.
        state (States): The relationship to the parent state.
        country (Countries): The relationship to the parent country.
    """
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    state_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('states.id'), nullable=False)
    state_code: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'), nullable=False)
    country_code: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=False)
    latitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(10, 8), nullable=False)
    longitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(11, 8), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default='2014-01-01 12:01:01')
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    state: so.Mapped['States'] = so.relationship(foreign_keys=[state_id])
    country: so.Mapped['Countries'] = so.relationship(foreign_keys=[country_id])

    def __repr__(self):
        return f'<City {self.name}>'


