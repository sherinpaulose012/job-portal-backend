from django.db.models import Count
from django.core.cache import cache

from applications.models import Application


class AnalyticsService:

    def hiring_funnel(self):

        total = Application.objects.count()

        shortlisted = Application.objects.filter(
            status="SHORTLISTED"
        ).count()

        interviewed = Application.objects.filter(
            status="INTERVIEWED"
        ).count()

        selected = Application.objects.filter(
            status="SELECTED"
        ).count()

        return {
            "applied": total,
            "shortlisted": shortlisted,
            "interviewed": interviewed,
            "selected": selected
        }

    def conversion_ratio(self):

        funnel = self.hiring_funnel()

        applied = funnel["applied"]

        if applied == 0:
            return 0

        return round(
            (funnel["selected"] / applied) * 100,
            2
        )

    def job_performance(self):

        jobs = (
            Application.objects
            .select_related("job")
            .values("job__title")
            .annotate(
                applications=Count("id")
            )
        )

        return list(jobs)

    def role_metrics(self):

        roles = (
            Application.objects
            .select_related("job")
            .values("job__job_type")
            .annotate(
                total=Count("id")
            )
        )

        return list(roles)

    def dashboard(self):

        cached = cache.get("analytics_dashboard")

        if cached:
            return cached

        data = {

            "hiring_funnel":
                self.hiring_funnel(),

            "conversion_ratio":
                self.conversion_ratio(),

            "job_performance":
                self.job_performance(),

            "role_metrics":
                self.role_metrics()

        }

        cache.set(
            "analytics_dashboard",
            data,
            timeout=300
        )

        return data