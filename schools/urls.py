from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'schools.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'grades.views.report_sheet', name='report-sheet'),

    url(r'^admin/', include(admin.site.urls)),
)
