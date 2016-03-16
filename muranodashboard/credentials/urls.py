#    Copyright (c) 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import urls
from muranodashboard.credentials import views


urlpatterns = urls.patterns(
    '',
    urls.url(r'^$', views.CloudCredentialsView.as_view(),
             name='index'),

    urls.url(r'^add$', views.AddCloudCredentialView.as_view(),
             name='add'),

    urls.url(r'^delete$', views.CloudCredentialsView.as_view(),
             name='delete'),

)
