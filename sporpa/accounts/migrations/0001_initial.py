# Generated by Django 4.1 on 2022-08-28 17:51

from django.db import migrations, models

import accounts.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this record should be treated as active. Unselect this instead of deleting records.",
                        verbose_name="active",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="created at")),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="Enter a datetime instead when you delete the record.",
                        null=True,
                        verbose_name="deleted at",
                    ),
                ),
                ("first_name", models.CharField(max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(max_length=150, verbose_name="last name")),
                (
                    "email",
                    models.EmailField(
                        error_messages={"unique": "A user with that email already exists."},
                        max_length=254,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to=accounts.models.user.user_directory_path),
                ),
                ("birthdate", models.DateField(null=True, verbose_name="birthdate")),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Unspecified"), (1, "Male"), (2, "Female")], default=0, verbose_name="gender"
                    ),
                ),
                ("about", models.TextField(blank=True, max_length=600, verbose_name="about")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "user",
            },
            managers=[
                ("objects", accounts.models.user.UserManager()),
                ("all_objects", accounts.models.user.UserManager(all_objects=True)),
            ],
        ),
    ]
