import django_filters

from .models import Job


class JobFilter(
    django_filters.FilterSet
):

    skills = django_filters.CharFilter(
        field_name="skills",
        lookup_expr="icontains"
    )

    location = django_filters.CharFilter(
        field_name="location",
        lookup_expr="icontains"
    )

    class Meta:

        model = Job

        fields = {
            "experience": ["exact"],
            "salary_min": ["exact"],
            "salary_max": ["exact"],
            "job_type": ["exact"],
        }