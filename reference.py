from django.db import models


class SampleModel(models.Model):
    # Basic fields
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    name = models.CharField(max_length=100)  # Character field
    email = models.EmailField(unique=True)  # Email field
    age = models.PositiveIntegerField(null=True, blank=True)  # Positive integer field

    # Text fields
    description = models.TextField()  # Large text field

    # Date and time fields
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated
    birthdate = models.DateField(null=True, blank=True)  # Date field

    # Boolean fields
    is_active = models.BooleanField(default=True)  # Boolean field

    # File and image fields
    profile_picture = models.ImageField(
        upload_to="profiles/", null=True, blank=True
    )  # Image field
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)  # File field

    # Choices field
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("suspended", "Suspended"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )  # Choices field

    # ForeignKey field
    related_model = models.ForeignKey(
        "AnotherModel", on_delete=models.CASCADE, null=True, blank=True
    )

    # Many-to-Many field
    tags = models.ManyToManyField("TagModel", blank=True)  # Many-to-Many field

    def __str__(self):
        return self.name


class AnotherModel(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class TagModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
