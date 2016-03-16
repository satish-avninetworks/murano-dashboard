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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tables
from muranoclient.common import exceptions as exc
from oslo_log import log as logging

from muranodashboard import api

LOG = logging.getLogger(__name__)


class AddCloudCredentials(tables.LinkAction):
    name = "add_category"
    verbose_name = _("Add Credentials")
    url = "horizon:murano:credentials:add"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteCloudCredentials(tables.DeleteAction):
    data_type_singular = _('Credentials')
    data_type_plural = _('Credentials')

    def allowed(self, request, category=None):
        if category is not None:
            if not category.package_count:
                return True
        return False

    def delete(self, request, obj_id):
        try:
            api.muranoclient(request).credentials.delete(obj_id)
        except exc.HTTPException:
            LOG.exception(_('Unable to delete category'))
            url = reverse('horizon:murano:credentials:index')
            exceptions.handle(request,
                              _('Unable to delete category.'),
                              redirect=url)


class CloudCredentialsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Credentials Name'))
    package_count = tables.Column('package_count',
                                  verbose_name=_('Package Count'))

    class Meta(object):
        name = 'credentials'
        verbose_name = _('Application Credentials')
        table_actions = (AddCloudCredentials,)
        row_actions = (DeleteCloudCredentials,)
        multi_select = False
