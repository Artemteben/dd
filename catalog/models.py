from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование")
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to='catalog/image',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.IntegerField(
        verbose_name="Цена за покупку"
    )
    created_at = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateField(
        blank=True, null=True, verbose_name="Дата последнего изменения"
    )

    def __str__(self):
        return self.name

    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="Счётчик просмотров",
        help_text="Укажите количество просмотров",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    content = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="catalog/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите фото продукта",
    )
    date_creation = models.DateField(verbose_name="Дата создания", blank=True, null=True)
    publication_sign = models.BooleanField(verbose_name="Уже опубликовано ?", default=False)
    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="Счётчик просмотров",
        help_text="Укажите количество просмотров",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:blog_detail", kwargs={"pk": self.pk, "slug": self.slug})

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["publication_sign", "-date_creation"]
