import streamlit as st
from sweet_shop import Sweet, SweetShopManagementSystem
import pandas as pd
import json

st.set_page_config(layout='wide')

DATA_FILE = 'sweets.json'

def load_inventory():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            sweets = [Sweet.from_dict(s) for s in data['sweets']]
            system = SweetShopManagementSystem()
            system.sweets = sweets
            return system
    except FileNotFoundError:
        return SweetShopManagementSystem()

def save_inventory(system):
    data = {
        'sweets': [s.to_dict() for s in system.sweets]
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

if 'system' not in st.session_state:
    st.session_state.system = load_inventory()

system = st.session_state.system

st.title('🍬 Sweet Shop Management Dashboard')

# All sweets table
st.header('📋 Current Inventory')
sweets_data = [{'ID': s.id, 'Name': s.name, 'Category': s.category, 'Price': f'₹{s.price}', 'Quantity': s.quantity} for s in system.view_all()]
st.dataframe(pd.DataFrame(sweets_data), use_container_width=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(['🍭 ADD SWEET', '🗑️ DELETE SWEET', '🔍 SEARCH SWEETS', '🛒 PURCHASE', '📦 RESTOCK'])

with tab1:
    st.header('🍭 Add New Sweet')
    if 'add_form_key' not in st.session_state:
        st.session_state.add_form_key = 0
    with st.container():
        st.info('Tip: Sweet names must be unique (case-insensitive).')
        with st.expander('Add Form', expanded=True):
            with st.form(key=f'add_sweet_form_{st.session_state.add_form_key}'):
                st.markdown('# Enter Details')
                name = st.text_input('Name', help='Unique name for the sweet')
                category = st.selectbox('Category', ['Nut-Based', 'Vegetable-Based', 'Milk-Based', 'Chocolate', 'Sugar-Based'], key='add_category', help='Choose from predefined categories')
                col_price, col_qty = st.columns(2)
                price = col_price.number_input('Price', min_value=0, step=1, help='Price per unit (positive integer)')
                quantity = col_qty.number_input('Quantity', min_value=1, step=1, help='Initial stock (at least 1)')
                submitted = st.form_submit_button('Add Sweet')
                if submitted:
                    if not name.strip():
                        st.error('Name is required')
                    elif any(s.name.lower() == name.lower() for s in system.view_all()):
                        st.error('Sweet name already exists')
                    elif price <= 0:
                        st.error('Price must be greater than 0')
                    elif quantity <= 0:
                        st.error('Quantity must be greater than 0')
                    else:
                        system.add_sweet(name, category, price, quantity)
                        save_inventory(system)
                        st.success(f'Added {name} successfully!')
                        st.session_state.add_form_key += 1
                        st.rerun()

with tab2:
    st.header('🗑️ Delete Sweet')
    with st.container():
        st.info('Tip: Deleting removes the sweet permanently.')
        with st.expander('Delete Form', expanded=True):
            st.markdown('# Delete by ID')
            sweet_id = st.number_input('ID to delete', min_value=1001, step=1, format='%d', help='Enter the ID from the inventory table')
            def handle_delete():
                try:
                    system.delete_sweet(int(sweet_id))
                    save_inventory(system)
                    st.session_state.delete_success = True
                except ValueError as e:
                    st.session_state.delete_error = str(e)
            st.button('Delete Sweet', on_click=handle_delete)
            if 'delete_success' in st.session_state:
                st.success(f'Deleted sweet with ID {sweet_id}')
                del st.session_state.delete_success
                st.rerun()
            if 'delete_error' in st.session_state:
                st.error(st.session_state.delete_error)
                del st.session_state.delete_error

with tab3:
    st.header('🔍 Search Inventory')
    with st.container():
        st.info('Tip: Searches are partial and case-insensitive.')
        with st.expander('Search Options', expanded=True):
            st.markdown('# Search Criteria')
            search_type = st.selectbox('Search by', ['Name', 'Category', 'Price Range'], key='search_type', help='Choose search type')
            if search_type == 'Name':
                sweet_names = [''] + [s.name for s in system.view_all()]
                selected_name = st.selectbox('Select Name', sweet_names, key='search_name', help='Partial match on name')
                if selected_name:
                    results = system.search_by_name(selected_name)
                else:
                    results = []
            elif search_type == 'Category':
                categories = [''] + ['Nut-Based', 'Vegetable-Based', 'Milk-Based', 'Chocolate', 'Sugar-Based']
                selected_category = st.selectbox('Select Category', categories, key='search_category', help='Partial match on category')
                if selected_category:
                    results = system.search_by_category(selected_category)
                else:
                    results = []
            else:
                col_min, col_max = st.columns(2)
                min_price = col_min.number_input('Min Price', min_value=0, help='Minimum price (inclusive)')
                max_price = col_max.number_input('Max Price', min_value=0, value=1000, help='Maximum price (inclusive)')
                results = system.search_by_price_range(min_price, max_price)
            if st.button('Search'):
                if results:
                    st.header('Search Results')
                    search_data = [{'ID': s.id, 'Name': s.name, 'Category': s.category, 'Price': f'₹{s.price}', 'Quantity': s.quantity} for s in results]
                    st.dataframe(pd.DataFrame(search_data), use_container_width=True)
                else:
                    st.info('No results found.')

with tab4:
    st.header('🛒 Purchase Sweet')
    with st.container():
        st.info('Tip: Cannot purchase more than available stock.')
        with st.expander('Purchase Form', expanded=True):
            st.markdown('# Purchase Details')
            sweet_options = [f'{s.name} ({s.id}) - Qty: {s.quantity}' for s in system.view_all()]
            selected = st.selectbox('Select Sweet', sweet_options, key='purchase_select', help='Choose from available sweets')
            qty = st.number_input('Quantity to Purchase', min_value=1, help='Amount to buy (positive integer)')
            if st.button('Confirm Purchase') and selected:
                try:
                    sweet_id = int(selected.split('(')[1].split(')')[0])
                    system.purchase(sweet_id, qty)
                    save_inventory(system)
                    st.success('Purchase successful!')
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

with tab5:
    st.header('📦 Restock Sweet')
    with st.container():
        st.info('Tip: Restock adds to existing quantity.')
        with st.expander('Restock Form', expanded=True):
            st.markdown('# Restock Details')
            sweet_options = [f'{s.name} ({s.id}) - Qty: {s.quantity}' for s in system.view_all()]
            selected = st.selectbox('Select Sweet', sweet_options, key='restock_select', help='Choose sweet to restock')
            qty = st.number_input('Quantity to Restock', min_value=1, help='Amount to add (positive integer)')
            if st.button('Confirm Restock') and selected:
                try:
                    sweet_id = int(selected.split('(')[1].split(')')[0])
                    system.restock(sweet_id, qty)
                    save_inventory(system)
                    st.success('Restock successful!')
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

st.markdown('---')
st.caption('Powered by Streamlit | Data persists in sweets.json') 