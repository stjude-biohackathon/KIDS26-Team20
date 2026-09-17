from django.db import migrations, models


def add_library_type_if_missing(apps, schema_editor):
    table_name = 'mygpt_backend_dataset'
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]

    if 'library_type' in columns:
        return

    Dataset = apps.get_model('mygpt_backend', 'Dataset')
    field = models.CharField(max_length=20, default='papers')
    field.set_attributes_from_name('library_type')
    schema_editor.add_field(Dataset, field)


def remove_library_type_if_present(apps, schema_editor):
    table_name = 'mygpt_backend_dataset'
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]

    if 'library_type' not in columns:
        return

    Dataset = apps.get_model('mygpt_backend', 'Dataset')
    field = models.CharField(max_length=20, default='papers')
    field.set_attributes_from_name('library_type')
    schema_editor.remove_field(Dataset, field)


class Migration(migrations.Migration):

    dependencies = [
        ('mygpt_backend', '0056_alter_answer_rating'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_library_type_if_missing, remove_library_type_if_present),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='dataset',
                    name='library_type',
                    field=models.CharField(default='papers', max_length=20),
                ),
            ],
        ),
    ]