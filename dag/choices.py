FIELDTYPES = (
    ('CharField', 'CharField'),
    ('IntegerField', 'IntegerField'),
    ('TextField', 'TextField'),
    ('DateField', 'DateField'),
    ('BooleanField', 'BooleanField'),
    ('DecimalField', 'DecimalField'),
    ('ForeignKey', 'ForeignKey'),
    ('TextField', 'TextField'),
    ('NullBooleanField', 'NullBooleanField'),
    ('DateTimeField', 'DateTimeField'),
)


BUSINESS_RULE_FUNCTIONS = (
    ('MODEL_SAVE', 'MODEL_SAVE'),
    ('FORM_INIT', 'FORM_INIT'),
    ('FORM_CLEAN', 'FORM_CLEAN'),
    ('ADMIN_CUSTOM_FILTER', 'ADMIN_CUSTOM_FILTER'),
    ('ADMIN_CUSTOM_COLUMN', 'ADMIN_CUSTOM_COLUMN'),
)


INLINE_TYPE = (
    ('TabularInline', 'TabularInline'),
    ('StackedInline', 'StackedInline'),
)
