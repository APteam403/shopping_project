prompt = """
Here is the results of a skin care quiz, designed to figure out the best skin care routine,
and the best set of products the user can use. 
Age: {age}
Sex: {sex}
local Weather condition: {weather}
Skin Type: {skin_type}
Skin Moisture: {skin_moisture}
Skin Texture: {skin_texture}
Skin Sensitivity Level: {skin_sensitivity}
Sun Exposure Level: {sun_exposure}
Favorite Product Type: {favorite_product_type}
Allergic Substances(if any, blank if none exists): {if_allergic}

Here are the products we have in our store,
however only the ones that their is_active field is equal to True(1) should be used in the generated routine:
{products}
(the following fields should be considered for recommending the products:
name, brand, description, category, skin_type, concerns_targeted, slug, and tags.
after considering the above fields, the products' slug should be saved to be used later.)

Please:
1. Analyze the quiz results.
2. Recommend three detailed routines. the first one should be a full plan routine, with 5 or more steps
(each step is considered as one product) alongside the time of the day and how many times the product should be used,
and the way it should be used. the second routine should be a hydration plan routine, focused on the products
that target skin hydration alongside the time of the day and how many times the product should be used,
and the way it should be used. the third routine should be a minimalist plan, which is a basic 3-step routine and 
minimal instructions on how and when the products should be used. 
3. using the slugs saved before, hyperlink the text of the title of each step in the generated routine above.
(the link to the product would be like this ==> http://127.0.0.1:8000/store/detail/slug )
Return the answer as JSON in the following format:
{{
    "routine": "string",
}}  
(note that the generated routine string should be completely written in farsi(persian), and the title of each step,
should be hyperlinked to the recommended product for that step(according to the instructions provided above).
"""