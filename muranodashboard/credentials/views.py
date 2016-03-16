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

import itertools

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon.forms import views
from horizon import tables as horizon_tables
from horizon.utils import functions as utils

from muranodashboard import api
from muranodashboard.credentials import forms
from muranodashboard.credentials import tables


class CloudCredentialsView(horizon_tables.DataTableView):
    table_class = tables.CloudCredentialsTable
    template_name = 'cloudcredentials/index.html'

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        prev_marker = self.request.GET.get(
            tables.CloudCredentialsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            sort_dir = 'asc'
            marker = prev_marker
        else:
            sort_dir = 'desc'
            marker = self.request.GET.get(
                tables.CloudCredentialsTable._meta.pagination_param, None)

        page_size = utils.get_page_size(self.request)

        request_size = page_size + 1
        kwargs = {'filters': {}}
        if marker:
            kwargs['marker'] = marker
        kwargs['sort_dir'] = sort_dir

        credentials = []
        self._prev = False
        self._more = False
        with api.handled_exceptions(self.request):
            credentials_iter = api.muranoclient(self.request).credentials.list(
                limit=request_size, **kwargs)

            credentials = list(itertools.islice(credentials_iter, request_size)
                               )
            # first and middle page condition
            if len(credentials) > page_size:
                credentials.pop(-1)
                self._more = True
                # middle page condition
                if marker is not None:
                    self._prev = True
            # first page condition when reached via prev back
            elif sort_dir == 'asc' and marker is not None:
                self._more = True
            # last page condition
            elif marker is not None:
                self._prev = True
            if prev_marker is not None:
                credentials.reverse()
        return credentials


class AddCloudCredentialView(views.ModalFormView):
    form_class = forms.AddCredentialForm
    form_id = 'add_category_form'
    modal_header = _('Add Credential')
    template_name = 'credentials/add.html'
    context_object_name = 'category'
    page_title = _('Add Application Credential')
    success_url = reverse_lazy('horizon:murano:credentials:index')
    submit_label = _('Add')
    submit_url = reverse_lazy('horizon:murano:credentials:add')
