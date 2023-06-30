from flask import Flask, request, url_for, render_template, redirect
import helper.py

app=Flask(__name__)

@app.route('/')
@app.route('/items')
def get_all_items():
    # Get items from the helper
    try:
        items=helper.get_all_items()        
    except Exception as e:
        print(f"Could not get items")
    finally:
        return render_template('items.html', items=items)

@app.route('/add_task')
def add_task():
    return render_template("add_task.html")

@app.route('/save_task', methods=['POST'])
def save_task():
    # Get item from the POST body
    item=request.form['item']
    stat=request.form['stat']
    
    try:
        helper.add_to_list(item, stat)
    except Exception as e:
        print(f"Could not add item")
    finally:
        return redirect('/items')


@app.route('/item/stat', methods=['GET'])
def get_item():
    # Get parameter from the URL
    item = request.args.get('name')

    # Get items from the helper
    stat = helper.get_item(item)

    # Return 404 if item not found
    if stat is None:
        print("Item not found")
    return render_template('item.html', item=item, stat=stat)

@app.route('/edit_task/<string:item>')
def edit_task(item):
    
    try:        
        stat=helper.get_status(item)  
        
    except Exception as e:
        print(f"A error appears: {e} ")
    finally:
        return render_template('edit_task.html', item=item, stat=stat)
    
@app.route('/item/update', methods=['POST'])
def update_status():
    # Get item from the POST body
    item=request.form['item']
    stat=request.form['stat']
    # Update item in the list
    try:        
        helper.update_status(item, stat)
        print("try! update")
        print(item, stat)
    # Return error if the status could not be updated
    except Exception as e:
        print(f"Could not update {e}")
    finally:
        return redirect('/items')
        
@app.route('/item/remove', methods=['POST'])
def delete_item():
        
    # Delete item from the list
    try:
        helper.delete_item(request.form['item'])
    except Exception as e:
        print(f"Could not delete: {e}")
    finally:
        return redirect('/items')
 
@app.route("/input")
def input():
    statusList=helper.execute("SELECT * FROM status order by stat")
    return render_template("input.html", statusList=statusList )   

if __name__=='__main__':
    app.run(debug=True)