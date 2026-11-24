import os
from django import forms
from .models import Evidence, Category

ALLOWED_EXTENSIONS = [
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff',
    # Videos
    '.mp4', '.mov', '.avi', '.mkv', '.webm',
    # Audio
    '.mp3', '.wav', '.ogg', '.m4a', '.flac',
    # Documents
    '.pdf', '.doc', '.docx', '.txt', '.csv', '.xlsx', '.log',
    # Archives / Forensic disk images
    '.zip', '.tar', '.gz', '.7z', '.raw', '.dd', '.img'
]

MAX_FILE_SIZE_MB = 100

class EvidenceUploadForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ['title', 'description', 'category', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descriptive Title (e.g. Crime Scene Surveillance Angle 1)',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed context, seizure location, chain of custody remarks...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'evidenceFileInput',
                'required': True
            })
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file format '{ext}'. Allowed types: images, audio, video, documents, forensic archives."
                )
            if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(f"File size exceeds maximum permitted limit ({MAX_FILE_SIZE_MB} MB).")
        return uploaded_file


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description', 'icon']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Category scope...'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FontAwesome icon e.g. fa-image, fa-film, fa-file-pdf'}),
        }


class EvidenceSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Evidence ID (e.g. 101, E101) or Title keyword...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses'), ('Pending', 'Pending'), ('Verified', 'Verified'), ('Rejected', 'Rejected')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    algorithm = forms.ChoiceField(
        choices=[
            ('c_binary', 'C Binary Search O(log n)'),
            ('c_hash', 'C Hash Table O(1)'),
            ('c_bst', 'C Binary Search Tree'),
            ('c_linear', 'C Linear Search O(n)')
        ],
        required=False,
        initial='c_binary',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
