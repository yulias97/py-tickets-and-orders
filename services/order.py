from datetime import datetime
from typing import Iterable

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(
        username: str | None = None
) -> Iterable:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()