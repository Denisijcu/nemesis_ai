<section class="py-12 bg-gray-50">
    <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-12">Lo que dicen nuestros clientes</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for testimonial in testimonials %}
            <div class="bg-white p-6 rounded-lg shadow-lg">
                <div class="flex items-center mb-4">
                    <!-- Avatar por defecto si no hay uno en Google Sheets -->
                    <img src="{{ testimonial.avatar if testimonial.avatar else 'https://via.placeholder.com/48' }}" 
                         alt="{{ testimonial.name }}" 
                         class="w-12 h-12 rounded-full object-cover mr-4">
                    <div>
                        <h3 class="font-bold text-lg">{{ testimonial.name }}</h3>
                        <div class="flex text-yellow-400">
                            <!-- Si tienes un campo "rating" en Google Sheets, úsalo aquí -->
                            {% for _ in range(testimonial.rating|int) %}
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                            </svg>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <p class="text-gray-600 italic">{{ testimonial.comment }}</p>
                <p class="text-gray-400 text-sm mt-4">{{ testimonial.timestamp }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>