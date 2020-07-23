from rest_framework import serializers

from home.models import Banner, Navbar


class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("img", 'link')

class NavbarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar
        fields = ("title", 'link','position','is_site')

# class NavbarBut(serializers.ModelSerializer):
#     class Meta:
#         model = Navbar
#         fields = ("title", 'link','position')
