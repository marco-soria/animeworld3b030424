class Cart:
    
    def __init__(self,request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        total = self.session.get('cart_total')
        if not cart:
            cart = self.session['cart'] = {}
            total = self.session['cart_total'] = 0
            
        self.cart = cart
        self.total = float(total)
        
    def add(self,product,quantity, image=None):
        if (str(product.id) not in self.cart.keys()):
            self.cart[product.id] = {
                'product_id':product.product_id,
                'name':product.product_name,
                'quantity':quantity,
                'price':str(product.product_price),
                'image':image if image else product.product_image.url,
                'category':product.category_id.category_name,
                'subtotal':str(quantity * product.product_price)
            }
        else:
            for key,value in self.cart.items():
                if key == str(product.product_id):
                    value['quantity'] = value['quantity']  + quantity
                    value['subtotal'] = str(float(value['quantity']) * float(value['price']))
                    break           
            
        self.save()
        
    def delete(self,product):
        if str(product.product_id) in self.cart:
            del self.cart[str(product.product_id)]
            self.save()  
            
    def clear(self):
        self.session['cart'] = {}
        self.session['cart_total'] = 0   
    
    def save(self):
        total = 0
        for key,value in self.cart.items():
            total += float(value['subtotal'])
            
        self.session['cart_total'] = total
        self.session['cart'] = self.cart
        self.session.modified = True
        
    