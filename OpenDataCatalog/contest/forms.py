from django import forms


class EntryForm(forms.Form):
    """
    Form for submitting an entry to a contest.
    """
    org_name = forms.CharField(max_length=255, label="Organization Name")
    org_url = forms.CharField(max_length=255, label="Organization Url")
    contact_person = forms.CharField(max_length=150, label="Contact Person")
    contact_phone = forms.CharField(max_length=15, label="Contact Phone Number")
    contact_email = forms.EmailField(max_length=150, label="Contact Email")
    data_set = forms.CharField(max_length=255, label="Data Set to Nominate")
    data_use = forms.CharField(max_length=1000, widget=forms.Textarea, label="If this data set were available, how would your organization use it?")
    data_mission = forms.CharField(max_length=1000, widget=forms.Textarea, label="How would this data set contribute to your organization's mission")


