from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from models import CarListing
from models import HttpResponseForbidden
from models import Listing
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUserOrReadOnly

from backend.core import db
from forms import ListingForm
from .models import Listing, User, Role, Account, Ad
from .permissions import IsAdminUserOrReadOnlyForListings
from .serializers import AdSerializer
from ..apps.auth.serializers import UserSerializer


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'create_listing.html', {'form': form})

def edit_listing(request, pk):
    listing = Listing.objects.get(pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'edit_listing.html', {'form': form, 'listing': listing})

def listing_details(request, listing_id):
    listing = get_object_or_404(CarListing, pk=listing_id)
    if request.user.account_type == 'premium' and listing.seller == request.user:
        # Logic to calculate and display the view statistics and average prices
        context = {
            'listing': listing,
            'views': listing.views,
            'views_today': listing.views_today,
            'views_this_week': listing.views_this_week,
            'views_this_month': listing.views_this_month,
            'average_price_region': listing.average_price_region,
            'average_price_city': listing.average_price_city,
            'average_price_country': listing.average_price_country
        }
        return render(request, 'listing_details_premium.html', context)
    else:
        return HttpResponseForbidden("You do not have permission to view this listing's details")

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    listing = db.relationship('Listing', backref=db.backref('views', lazy=True))
    user = db.relationship('User', backref=db.backref('views', lazy=True))

    def __repr__(self):
        return f"<View {self.listing_id} {self.user_id} {self.created_at}>"


class ListingSerializer:
    pass


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class ListingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAdminUserOrReadOnlyForListings]

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrReadOnlyForListings]


class RoleSerializer:
    pass


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUserOrReadOnlyForListings]


class AccountSerializer:
    pass


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUserOrReadOnlyForListings]
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
