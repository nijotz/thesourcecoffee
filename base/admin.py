def get_admin_site(BaseAdminSite):
    class AdminSite(BaseAdminSite):
        
        def index(self, *args, **kwargs):
            import ipdb; ipdb.set_trace()
            response = super(AdminSite, self).index(*args, **kwargs)
            #app_list = response.context_data['app_list']
            #app_list = []
            #response.context_data['app_list'] = []
            return response

            try:
                idx = app_list.index('orders')
                orders_app = app_list[idx]
                orders_app['models'].append('what')
            except:
                pass
            raise(Exception)
            return response

    return AdminSite()
