from django.shortcuts import redirect, render  #render - return an HttpResponse object 
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests
    import json

    if request.method =='POST':
        ticker = request.POST.get('ticker')
        # Replace 'your_finnhub_api_key' with your actual Finnhub API key
        api_key = 'cqs4vhpr01quefai7lngcqs4vhpr01quefai7lo0'
        
        # API endpoints
        api1 = "https://finnhub.io/api/v1/stock/profile2?symbol=" + ticker + "&token=cqs4vhpr01quefai7lngcqs4vhpr01quefai7lo0"
        api2 = "https://finnhub.io/api/v1/quote?symbol=" + ticker + "&token=cqs4vhpr01quefai7lngcqs4vhpr01quefai7lo0"
    
         # Make API requests
        api_request1 = requests.get(api1)
        api_request2 = requests.get(api2)
    
        try:
        # Parse JSON responses
            api1 = json.loads(api_request1.content)
            api2 = json.loads(api_request2.content)

        # if not api1_data:
        #     api1_data = {"error": "No data available for the company overview."}
        # if not api2_data:
        #     api2_data = {"error": "No data available for the stock information."}
        except Exception as e:
           
            api1 = "Error..."
            api2 = "Error..."
        return render(request, 'home.html', {'api1': api1, 'api2': api2})

    else:
        return render(request, 'home.html', {
        'ticker':"Enter a Ticker symbol"
    }) 

   
def add_stock(request): #request: The HttpRequest object. It tells the render function about the request context.
    if request.method =='POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock Added Successfully")
            return redirect('add_stock')  # Redirect to avoid resubmission on refresh
        else:
            messages.error(request, "There was an error with your form submission")
    else:
        form = StockForm()  # Initialize the form for GET requests

    # Fetch all stocks to display, or use the form context if needed
    ticker = Stock.objects.all()
    return render(request, 'add_stock.html', {'form': form, 'ticker': ticker})  
    
def delete(request, stock_id): #request: The HttpRequest object. It tells the render function about the request context.
    item = Stock.objects.get(pk=stock_id) 
    item.delete()
    messages.success(request,("Stock has been deleted"))
    return redirect('add_stock')
def about(request): #request: The HttpRequest object. It tells the render function about the request context.
    return render(request, 'about.html',{})