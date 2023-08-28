

class SearchConstants:
    STRING=['exact','iexact','contains','icontains','in','gt','gte','lt','lte','startswith','istartswith','endswith','iendswith','isnull']
    INT=['exact','iexact','contains','icontains','in','gt','gte','lt','lte','startswith','istartswith','endswith','iendswith','isnull']
    DATETIME=['exact','iexact','gt','gte','lt','lte','date','time','year','month','day','week','hour','minute','second','isnull' \
    ,'date__gt','time__gt','year__gt','month__gt','day__gt','week__gt','hour__gt','minute__gt','second__gt' \
    ,'date__gte','time__gte','year__gte','month__gte','day__gte','week__gte','hour__gte','minute__gte','second__gte' \
    ,'date__lt','time__lt','year__lt','month__lt','day__lt','week__lt','hour__lt','minute__lt','second__lt' \
    ,'date__lte','time__lte','year__lte','month__lte','day__lte','week__lte','hour__lte','minute__lte','second__lte' \
    ,'week__gt','week__gte','week__lt','week__lte'
    ]
    BOOLEAN=['exact','iexact','isnull']
    FLOAT=['exact','iexact','contains','icontains','in','gt','gte','lt','lte','startswith','istartswith','endswith','iendswith','isnull']
    DECIMAL=['exact','iexact','contains','icontains','in','gt','gte','lt','lte','startswith','istartswith','endswith','iendswith','isnull']
    UUID=['exact','iexact','contains','icontains','in','gt','gte','lt','lte','startswith','istartswith','endswith','iendswith','isnull']
    DATE=['exact','iexact','gt','gte','lt','lte','year','month','day','week','week_day','quarter','range','in','isnull']

