from django import template
register = template.Library()

from django.apps import apps
from django.urls import reverse

@register.simple_tag(takes_context=True)
def menu2(context):
    request = context['request']
    user = request.user
    app_labels = []
    model_names = []
    model_urls = []
    cpvconsoletag = True
    accesscontrol = True

    if request.path == '/convert/':
        r = '<li class="nav-item"><a href="/convert/" class="nav-link active"><i class="nav-icon fas fa-tachometer-alt"></i> <p>Home</p></a></li>'
    else:
        r = '<li class="nav-item"><a href="/convert/" class="nav-link"><i class="nav-icon fas fa-tachometer-alt"></i> <p>Home</p></a></li>'


    for app in apps.get_app_configs():
        # print(f"App: {app.label}")
        app_labels.append(app)
        for model in app.get_models():
            if user.has_perm(f'{model._meta.app_label}.view_{model._meta.model_name}'):
                if cpvconsoletag:
                    if request.path == '/convert/':
                        r += '<li class="nav-item has-treeview"><a href="#" class="nav-link"><i class="nav-icon fas fa-edit"></i> <p>CPV Console</p><p><i class="fas fa-angle-right right"></i></p></a><ul class="nav nav-treeview">'
                    else:
                        r += '<li class="nav-item has-treeview menu-open"><a href="#" class="nav-link active"><i class="nav-icon fas fa-edit"></i> <p>CPV Console</p><p><i class="fas fa-angle-right right"></i></p></a><ul class="nav nav-treeview">'
                    cpvconsoletag=False

                # print(f"Model----><---------: {model.__name__}")

                model_names.append(model.__name__)
                # print(model.__name__)
                try:
                    # url = reverse(f"{app.label}:{model.__name__.lower()}_list")

                    url = f"{reverse('admin:index')}{app.label}/{model.__name__.lower()}"
                    # print(url)
                    if model.__name__ == 'CustomUser' or model.__name__ == 'CustomGroup':
                        if accesscontrol:
                            r += '<li class="nav-item has-treeview"><a href="#" class="nav-link"><i class="nav-icon fas"></i> <p>Access Control</p><p><i class="fas fa-angle-right right"></i></p></a><ul class="nav nav-treeview">'
                            accesscontrol = False
                        if model.__name__ == 'CustomGroup':
                            if request.path == url + '/':
                                r += '<li class="nav-item"><a href="' + url + '"  class="nav-link active"><i class="far fa-circle nav-icon"></i> Groups</a></li>'
                            else:
                                r += '<li class="nav-item"><a href="' + url + '"  class="nav-link"><i class="far fa-circle nav-icon"></i> Groups</a></li>'

                        # print(f"App--------->: {app.label}")
                        if model.__name__ == 'CustomUser':
                            if request.path == url + '/':
                                r += '<li class="nav-item"><a href="' + url + '" class="nav-link active"><i class="far fa-circle nav-icon"></i> Users</a></li>'
                            else:
                                r += '<li class="nav-item"><a href="' + url + '" class="nav-link"><i class="far fa-circle nav-icon"></i> Users</a></li>'

                    if model.__name__ == 'Add_Profile':
                        if request.path == url + '/':
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link active"><i class="far fa-circle nav-icon"></i> Config Profile</a></li>'
                        else:
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link"><i class="far fa-circle nav-icon"></i> Config Profile</a></li>'
                    if model.__name__ == 'audit_log':
                        if request.path == url + '/':
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link active"><i class="far fa-circle nav-icon"></i> Audit Logs</a></li>'
                        else:
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link"><i class="far fa-circle nav-icon"></i> Audit Logs</a></li>'
                    # if model.__name__ == 'CrontabSchedule':
                    #     if request.path == url + '/':
                    #         r += '<li class="nav-item"><a href="' + url + '" class="nav-link active"><i class="far fa-circle nav-icon"></i>Schedule Cron</a></li>'
                    #     else:
                    #         r += '<li class="nav-item"><a href="' + url + '" class="nav-link"><i class="far fa-circle nav-icon"></i>Schedule Cron</a></li>'
                    if model.__name__ == 'TaskResult':
                        if request.path == url + '/':
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link active"><i class="far fa-circle nav-icon"></i>Schedule Task Result</a></li>'
                        else:
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link"><i class="far fa-circle nav-icon"></i>Schedule Task Result</a></li>'
                    if model.__name__ == 'PeriodicTask':
                        if request.path == url + '/':
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link active"><i class="far fa-circle nav-icon"></i>Schedule Periodic Task</a></li>'
                        else:
                            r += '<li class="nav-item"><a href="' + url + '" class="nav-link"><i class="far fa-circle nav-icon"></i>Schedule Periodic Task</a></li>'

                    # print(f"URL==============: {url}")
                    model_urls.append(url)
                except AttributeError:
                    continue
        if app.label == 'users' and accesscontrol== False:
            r+= '</li></ul>'
    # print('App Labels: ',app_labels)

    # print('Model Names: ', model_names)
    # print('Model urls: ', model_urls)
    # print(request.path)
    # print(r)
    return r

