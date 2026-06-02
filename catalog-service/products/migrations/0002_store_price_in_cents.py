from decimal import Decimal, ROUND_HALF_UP

from django.db import migrations, models


def copy_price_to_cents(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        product.price_cents = int((Decimal(product.price) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        product.save(update_fields=['price_cents'])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_cents',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RunPython(copy_price_to_cents, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
