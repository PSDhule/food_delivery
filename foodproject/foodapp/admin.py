from django.contrib import admin

from .models import (
    Restaurant,
    Food,
    Address,
    Cart,
    Wishlist,
    Order,
    OrderItem,
    Review,
    Contact,
    comment
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'rating',
        'is_active',
        'created_at'
    )

    search_fields = (
        'name',
        'location'
    )

    list_filter = (
        'is_active',
    )

# ===== FOOD BULK ACTIONS ====#
def assign_pizza_hut(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter(name='Pizza Hut' 
    ).first() 
   
    if restaurant: 
        updated = queryset.update(    restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Pizza Hut.' 
        ) 
            
    else: 
        modeladmin.message_user( 
            request, 
            'Pizza Hut restaurant not found.', 
            level='ERROR' 
        ) 

assign_pizza_hut.short_description = ( 
    'Assign selected foods to Pizza Hut' 
) 

def assign_burger_king(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter(    name='Burger King' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Burger King.' 
        ) 
        
    else: 
        modeladmin.message_user( 
            request, 
            'Burger King restaurant not found.', level='ERROR' 
        ) 
        
assign_burger_king.short_description = ( 
    'Assign selected foods to Burger King' 
) 

def assign_biryani_house(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter( name='Biryani House' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Biryani House.' 
        ) 
    
    else: 
        modeladmin.message_user( 
            request, 
            'Biryani House restaurant not found.', level='ERROR' 
        ) 
        
assign_biryani_house.short_description = ( 
    'Assign selected foods to Biryani House' 
) 

def assign_nagpur_food_house(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter( name='Nagpur Food House' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Nagpur Food House.' 
        ) 
        
    else: 
        modeladmin.message_user( 
            request, 
            'Nagpur Food House restaurant not found.', level='ERROR' 
        ) 
            
assign_nagpur_food_house.short_description = ( 'Assign selected foods to Nagpur Food House' 
) 

def assign_mumbai_spice(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter( name='Mumbai Spice' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Mumbai Spice.' 
        ) 
        
    else: 
        
        modeladmin.message_user( 
            request, 'Mumbai Spice restaurant not found.', level='ERROR' 
        ) 
        
assign_mumbai_spice.short_description = ( 
    'Assign selected foods to Mumbai Spice' 
) 

def assign_nashik_spice(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter( name='Nashik Spice' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Nashik Spice.' 
        ) 
        
    else: 
        modeladmin.message_user( 
            request, 
            'Nashik Spice restaurant not found.', level='ERROR' 
        ) 
        
assign_nashik_spice.short_description = ( 
    'Assign selected foods to Nashik Spice' 
) 

def assign_delhi_darbar(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter( name='Delhi Darbar' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Delhi Darbar.' 
        ) 
        
    else: 
        modeladmin.message_user( 
            request, 
            'Delhi Darbar restaurant not found.', level='ERROR' 
        ) 
        
assign_delhi_darbar.short_description = ( 
    'Assign selected foods to Delhi Darbar' 
) 

def assign_bangalore_bites(modeladmin, request, queryset): 
    restaurant = Restaurant.objects.filter( name='Bangalore Bites' 
    ).first() 
    
    if restaurant: 
        updated = queryset.update( restaurant=restaurant 
        ) 
        
        modeladmin.message_user( 
            request, 
            f'{updated} food items assigned to Bangalore Bites.' 
        ) 
        
    else: modeladmin.message_user( 
        request, 
        'Bangalore Bites restaurant not found.', level='ERROR' 
    ) 
    
assign_bangalore_bites.short_description = ( 
    'Assign selected foods to Bangalore Bites' 
)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'restaurant',
        'rating',
        'is_available'
    )

    search_fields = (
        'name',
        'category'
    )

    list_filter = (
        'category',
        'is_available',
        'restaurant'
    )

    actions = [ 
        assign_pizza_hut, 
        assign_burger_king, 
        assign_biryani_house, assign_nagpur_food_house, assign_mumbai_spice, 
        assign_nashik_spice, 
        assign_delhi_darbar, 
        assign_bangalore_bites, 
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'full_name',
        'phone',
        'city',
        'pincode',
        'is_default'
    )

    search_fields = (
        'user__username',
        'full_name',
        'phone',
        'city'
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'food',
        'quantity',
        'added_at'
    )

    search_fields = (
        'user__username',
        'food__name'
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'food',
        'created_at'
    )

    search_fields = (
        'user__username',
        'food__name'
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'total',
        'payment_method',
        'payment_status',
        'status',
        'created_at'
    )

    search_fields = (
        'order_number',
        'user__username',
        'food_name'
    )

    list_filter = (
        'status',
        'payment_method',
        'payment_status',
        'created_at'
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'food',
        'quantity',
        'price',
        'total'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'food',
        'rating',
        'created_at'
    )

    list_filter = (
        'rating',
        'created_at'
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'created_at'
    )

    search_fields = (
        'name',
        'email'
    )


@admin.register(comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at'
    )

    search_fields = (
        'name',
        'comment'
    )