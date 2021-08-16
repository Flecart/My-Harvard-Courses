import re
import random
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django import forms


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


class entry_form(forms.Form):
    title = forms.CharField(label="title", 
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Page Title',
                    'class': "form-control"
                    }))

    content = forms.CharField(label="content", widget=forms.Textarea(
                attrs={
                    'placeholder': 'Page Content',
                    'class': "form-control"
                    }))


class search_answer():
    def __init__ (self):
        self.answers = []
        self.exactMatch = False

    def append(self, match):
        self.answers.append(match)

    def setUnique(self, title):
        self.answers = [title]


def check_matches(title):
    entries = list_entries()
    answer = search_answer()

    title = title.lower().strip()
    for entry in entries:
        entry_normalized = entry.lower()
        
        if (title == entry_normalized):
            answer.exactMatch = True
            answer.setUnique(entry)
            return answer

        if title in entry_normalized:
            answer.append(entry)

    return answer


def get_random_page():
    entries = list_entries()
    random.seed(datetime.now())
    random_index = random.randint(0, len(entries) - 1)

    return entries[random_index]

