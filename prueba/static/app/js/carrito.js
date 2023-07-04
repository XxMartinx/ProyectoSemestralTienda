// Obtiene una referencia a los elementos del DOM
const cartItemsElement = document.getElementById('cart-items');
const cartTotalElement = document.getElementById('cart-total');
const checkoutButton = document.getElementById('checkout-button');

// Crea una variable para almacenar los elementos del carrito de compras
let cartItems = [];

// Agrega un artículo al carrito
function addItemToCart(item) {
  cartItems.push(item);
  updateCart();
}

// Elimina un artículo del carrito
function removeItemFromCart(index) {
  cartItems.splice(index, 1);
  updateCart();
}

// Actualiza el carrito de compras
function updateCart() {
  // Limpia la lista de artículos en el carrito
  cartItemsElement.innerHTML = '';

  // Recorre los elementos del carrito y crea los elementos de la lista
  for (let i = 0; i < cartItems.length; i++) {
    const item = cartItems[i];
    const listItem = document.createElement('li');
    listItem.innerText = item;
    const removeButton = document.createElement('button');
    removeButton.innerText = 'Eliminar';
    removeButton.addEventListener('click', () => removeItemFromCart(i));
    listItem.appendChild(removeButton);
    cartItemsElement.appendChild(listItem);
  }

  // Actualiza el total del carrito
  cartTotalElement.innerText = calculateCartTotal();
}

// Calcula el total del carrito
function calculateCartTotal() {
  let total = 0;

  // Realiza el cálculo sumando el precio de cada artículo en el carrito
  // Aquí debes ajustar la lógica de acuerdo a tu estructura de datos y precios
  for (let i = 0; i < cartItems.length; i++) {
    const item = cartItems[i];
    // Por ejemplo, si tienes un campo "price" en tus objetos de artículo:
    // total += item.price;
  }

  return total;
}

// Manejador de evento para el botón de pago
checkoutButton.addEventListener('click', () => {
  // Aquí puedes agregar la lógica para procesar el pago, por ejemplo, redirigir a una página de pago
});