from datetime import date

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError('Нужно указать user_name')
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)  # пароль в виде хеша
        user.save(using=self._db)
        return user
    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField('Имя пользователя', max_length=150, unique=True)
    push_hash = models.CharField('Push-хеш', max_length=255, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['push_hash']
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    def __str__(self):
        return self.user_name


class Map(models.Model):
    name = models.CharField('Название карты', max_length=200)
    description = models.FileField('Файл с описанием', upload_to='maps/descriptions/', blank=True)
    location = models.CharField('Местность', max_length=200)
    # координаты границ карты: список точек, например
    # [{"lat": 55.75, "lon": 37.61}, {"lat": 55.76, "lon": 37.65}, ...]
    coordinates = models.JSONField('Координаты границ', default=list, blank=True)
    file = models.FileField('TIFF-файл карты', upload_to='maps/tiff/',
                            validators=[FileExtensionValidator(['tif', 'tiff'])])
    compr_file = models.FileField('JPG для отображения', upload_to='maps/jpg/',
                                       validators=[FileExtensionValidator(['jpg', 'jpeg'])])
    author = models.CharField('Автор карты', max_length=150)
    date_added = models.DateField('Дата добавления / год создания', default=date.today)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        ordering = ['-date_added']

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField('Название соревнования', max_length=200)
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='courses',
                            verbose_name='Карта')
    # points — ссылка на таблицу CoursePoint
    category = models.CharField('Возрастная группа', max_length=50)
    public = models.BooleanField('Доступно всем пользователям', default=False)
    # Нужны, чтобы public=False имело смысл («только создателю и приглашённым»).
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='created_courses',
                                verbose_name='Создатель')
    invited_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name='invited_courses',
                                           verbose_name='Приглашённые пользователи')
    class Meta:
        verbose_name = 'Дистанция'
        verbose_name_plural = 'Дистанции'
    def __str__(self):
        return f'{self.name} ({self.category})'
    def is_available_for(self, user):
        # Может ли пользователь видеть эту дистанцию
        if self.public:
            return True
        if not user.is_authenticated:
            return False
        return (self.creator_id == user.id or self.invited_users.filter(pk=user.pk).exists())


class CoursePoint(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='points',
                               verbose_name='Дистанция')
    number = models.PositiveSmallIntegerField('Номер КП')
    # координаты КП, например {"lat": 55.75, "lon": 37.61}
    coordinates = models.JSONField('Координаты КП')
    QR = models.FileField('QR-код для отметки', upload_to='courses/qr/', blank=True)
    class Meta:
        verbose_name = 'Контрольный пункт'
        verbose_name_plural = 'Контрольные пункты'
        ordering = ['course', 'number']
        constraints = [
            models.UniqueConstraint(fields=['course', 'number'], name='unique_point_number_in_course'),
        ]

    def __str__(self):
        return f'{self.course} — КП {self.number}'

class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='results', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results',
                               verbose_name='Дистанция')
    time = models.DurationField('Время прохождения')
    place = models.PositiveIntegerField('Место', null=True, blank=True)
    leader_time = models.DurationField('Время лидера', null=True, blank=True)
    # delta_time — ссылка на таблицу с отметками
    public = models.BooleanField('Доступно всем пользователям', default=False)
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        ordering = ['course', 'place']
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_result_per_user_and_course'),
        ]

    def __str__(self):
        return f'{self.user} — {self.course}: {self.time}'

    @property
    def punches(self):
        """Отметки КП этого пользователя на этой дистанции (таблица Punch)."""
        return Punch.objects.filter(user=self.user, course=self.course)


class Punch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='punches', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='punches',
                               verbose_name='Дистанция')
    point_number = models.PositiveSmallIntegerField('Номер КП')
    time = models.DateTimeField('Время отметки')

    class Meta:
        verbose_name = 'Отметка'
        verbose_name_plural = 'Отметки'
        ordering = ['time']
        constraints = [
            models.UniqueConstraint(fields=['user', 'course', 'point_number'],
                                    name='unique_punch_per_user_course_point'),
        ]
    def __str__(self):
        return f'{self.user} — {self.course}, КП {self.point_number}'
