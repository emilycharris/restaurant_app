def get_id():
    profiles = Profile.objects.all()
    for profile in profiles:
        print(profile.id)
