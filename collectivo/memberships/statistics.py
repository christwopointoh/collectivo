from django.db.models import Avg, Max, Sum

from .models import MembershipType


def calculate_statistics(membership_type: MembershipType):
    """Get statistics for this membership type."""
    try:
        memberships = membership_type.memberships.filter(
            date_ended__isnull=True,
        )
        statistics = {
            "memberships (without date_ended)": memberships.count(),
            "memberships with date_accepted": memberships.filter(
                date_accepted__isnull=False
            ).count(),
            **{
                f"memberships with status: {status.name}": memberships.filter(
                    status=status
                ).count()
                for status in membership_type.statuses.all()
            },
        }
        try:
            import collectivo.profiles

            statistics.update(
                {
                    f"memberships with person type: {status}": membership_type.memberships.filter(
                        user__profile__person_type=status
                    ).count()
                    for status in ["natural", "legal"]
                }
            )
        except ImportError:
            pass

        # Ended memberships
        statistics.update(
            {
                "ended memberships (with date_ended)": memberships.filter(
                    date_accepted__isnull=False
                ).count(),
            }
        )

        # Shares statistics
        statistics.update(
            {
                **membership_type.memberships.aggregate(Sum("shares_signed")),
                **membership_type.memberships.aggregate(Avg("shares_signed")),
                **membership_type.memberships.aggregate(Max("shares_signed")),
                **membership_type.memberships.aggregate(Sum("shares_paid")),
                **membership_type.memberships.aggregate(Avg("shares_paid")),
                **membership_type.memberships.aggregate(Max("shares_paid")),
            }
        )

    except Exception as e:
        statistics = {"error trying to calculate statistics": str(e)}
    return statistics
