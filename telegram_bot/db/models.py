import datetime

from tortoise import fields, models

from telegram_bot.config.config import TZ


class User(models.Model):
    user_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    registered_at = fields.DatetimeField(auto_now_add=True, description="Registration date")
    language = fields.CharField(max_length=5, description="Language code")
    last_start = fields.DatetimeField(auto_now_add=True, description="Last use date")
    use_count = fields.IntField(default=0)

    async def use_update(self):
        self.use_count += 1
        self.last_start = datetime.datetime.now(TZ)
        await self.save(update_fields=["last_start", "use_count"])

    @classmethod
    async def today_online(cls) -> float:
        now_data = datetime.datetime.now(TZ)
        day_count = await cls.filter(
            last_start__year=now_data.year,
            last_start__month=now_data.month,
            last_start__day=now_data.day,
        ).count()
        all_count = await cls.all().count()
        percent = (day_count / all_count) * 100
        return percent

    @classmethod
    async def date_users(cls, from_: str, to: str)->tuple:
        y1, m1, d1 = tuple(map(lambda x: int(x.strip()), from_.split(",")))
        y2, m2, d2 = tuple(map(lambda x: int(x.strip()), to.split(",")))
        date1 = datetime.date(y1, m1, d1)
        date2 = datetime.date(y2, m2, d2)
        if date1 == date2:
            users_count = await User.filter(
                registered_at__year=date1.year,
                registered_at__month=date1.month,
                registered_at__day=date1.day,
            ).count()
        else:
            users_count = await User.filter(registered_at__range=[date1, date2]).count()
        return users_count, date1, date2
