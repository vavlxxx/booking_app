from src.models.users import UsersOrm
from src.models.rooms import RoomsOrm
from src.models.hotels import HotelsOrm
from src.models.hotels import HotelsOrm
from src.models.hotels import HotelsOrm
from src.models.bookings import BookingsOrm
from src.models.additionals import AdditionalsOrm, RoomsAdditionalsOrm

from src.schemas.hotels import Hotel
from src.schemas.auth import User, UserFullInfo
from src.schemas.hotels import Hotel
from src.schemas.bookings import Booking
from src.schemas.rooms import FullRoomData, RoomsWithRels
from src.schemas.additionals import AdditionalsData, RoomsAdditionalsData

from src.repos.mappers.base import DataMapper


class HotelsMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsMapper(DataMapper):
    db_model = RoomsOrm
    schema = FullRoomData


class RoomsRelsMapper(RoomsMapper):
    schema = RoomsWithRels


class AdditionalsMapper(DataMapper):
    db_model = AdditionalsOrm
    schema = AdditionalsData


class RoomsAdditionalsMapper(DataMapper):
    db_model = RoomsAdditionalsOrm
    schema = RoomsAdditionalsData


class BookingsMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class AuthMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class AuthFullInfoMapper(AuthMapper):
    schema = UserFullInfo
