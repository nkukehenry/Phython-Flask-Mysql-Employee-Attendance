from database_models import Timelog, Timetotals
from app import mallow


class TimelogSchema(mallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Timelog


class TotalsSchema(mallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Timetotals
