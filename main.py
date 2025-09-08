import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Initialize Gemini client
@st.cache_resource
def get_gemini_client():
    return genai.Client()

def generate_enhanced_prompt(clothing_type="kurta", style_details=""):
    """Generate an enhanced prompt for better clothing replacement results"""
    base_prompt = f"""
    Please perform a precise clothing replacement on the person in the first image using the {clothing_type} from the second image. 

    Instructions:
    1. Carefully analyze the person's body posture, lighting, and proportions in the first image
    2. Replace ONLY the clothing items (shirt, pants, etc.) with the {clothing_type} from the second image
    3. Maintain the person's exact body shape, skin tone, facial features, and pose
    4. Ensure the new clothing fits naturally with proper draping and fabric physics
    5. Match the lighting conditions and shadows from the original image
    6. Preserve the background completely unchanged
    7. Keep the same image quality and resolution
    8. Make sure the clothing colors and patterns match the reference {clothing_type} exactly
    
    {style_details}
    
    The result should look photorealistic with seamless integration of the new clothing.
    """
    return base_prompt

def process_images(person_image, clothing_image, clothing_type, style_details):
    """Process images using Gemini API"""
    client = get_gemini_client()
    
    prompt = generate_enhanced_prompt(clothing_type, style_details)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt, person_image, clothing_image],
        )
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                st.write("**AI Response:**", part.text)
            elif part.inline_data is not None:
                generated_image = Image.open(BytesIO(part.inline_data.data))
                return generated_image
                
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="AI try-on by Yash Desai | Virtual Clothing Try-On AI Tool",
        page_icon="👔",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://yashddesai.com',
            'Report a bug': 'mailto:contact@yashddesai.com',
            'About': """
            # AI try-on by Yash Desai
            Transform anyone's outfit using AI! Upload a person's photo and a clothing item to see the magic happen.
            
            **Features:**
            - AI-powered clothing replacement
            - Multiple clothing types supported
            - High-quality image generation
            - Easy-to-use interface
            
            **Contact:** contact@yashddesai.com
            **Website:** https://yashddesai.com
            """
        }
    )
    
    # Add SEO meta tags
    st.markdown("""
    <head>
        <meta name="description" content="AI try-on by Yash Desai - Transform outfits virtually using advanced AI. Upload photos and try on clothes digitally with our cutting-edge virtual try-on technology.">
        <meta name="keywords" content="AI try-on, virtual clothing, fashion AI, outfit transformation, digital wardrobe, AI fashion, virtual fitting, clothing replacement, AI tool, Yash Desai">
        <meta name="author" content="Yash Desai">
        <meta name="robots" content="index, follow">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta property="og:title" content="AI try-on by Yash Desai | Virtual Clothing Try-On AI Tool">
        <meta property="og:description" content="Transform anyone's outfit using AI! Upload a person's photo and a clothing item to see the magic happen with our advanced virtual try-on technology.">
        <meta property="og:image" content="https://yashddesai.com/ai-tryon-preview.png">
        <meta property="og:url" content="https://yashddesai.com/ai-tryon">
        <meta property="og:type" content="website">
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="AI try-on by Yash Desai | Virtual Clothing Try-On AI Tool">
        <meta name="twitter:description" content="Transform anyone's outfit using AI! Upload a person's photo and a clothing item to see the magic happen with our advanced virtual try-on technology.">
        <meta name="twitter:image" content="https://yashddesai.com/ai-tryon-preview.png">
        <link rel="canonical" href="https://yashddesai.com/ai-tryon">
    </head>
    """, unsafe_allow_html=True)
    
    # Add structured data for SEO
    st.markdown("""
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "AI try-on by Yash Desai",
        "description": "Transform anyone's outfit using AI! Upload a person's photo and a clothing item to see the magic happen with our advanced virtual try-on technology.",
        "url": "https://yashddesai.com/ai-tryon",
        "applicationCategory": "FashionApplication",
        "operatingSystem": "Web Browser",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "creator": {
            "@type": "Person",
            "name": "Yash Desai",
            "email": "contact@yashddesai.com",
            "url": "https://yashddesai.com"
        },
        "featureList": [
            "AI-powered clothing replacement",
            "Virtual try-on technology",
            "High-quality image generation",
            "Multiple clothing types support"
        ],
        "keywords": "AI try-on, virtual clothing, fashion AI, outfit transformation, digital wardrobe",
        "datePublished": "2024-09-08",
        "softwareVersion": "1.0.0"
    }
    </script>
    """, unsafe_allow_html=True)
    
    st.title("👔 AI try-on by Yash Desai")
    st.markdown("Transform anyone's outfit using AI! Upload a person's photo and a clothing item to see the magic happen.")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        clothing_type = st.selectbox(
            "Clothing Type",
            ["kurta", "shirt", "t-shirt", "dress", "jacket", "sweater", "traditional wear"],
            index=0
        )
        
        style_details = st.text_area(
            "Additional Style Instructions (Optional)",
            placeholder="e.g., 'Make sure the kurta is well-fitted', 'Adjust the sleeves properly', etc.",
            height=100
        )
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Upload Person's Photo")
        person_file = st.file_uploader(
            "Choose an image of a person",
            type=['png', 'jpg', 'jpeg'],
            key="person"
        )
        
        if person_file is not None:
            person_image = Image.open(person_file)
            st.image(person_image, caption="Person's Photo", use_column_width=True)
    
    with col2:
        st.subheader("👕 Upload Clothing Item")
        clothing_file = st.file_uploader(
            f"Choose an image of the {clothing_type}",
            type=['png', 'jpg', 'jpeg'],
            key="clothing"
        )
        
        if clothing_file is not None:
            clothing_image = Image.open(clothing_file)
            st.image(clothing_image, caption=f"{clothing_type.title()} Reference", use_column_width=True)
    
    # Generate button
    if st.button("🎨 Generate New Look", type="primary", use_container_width=True):
        if person_file is not None and clothing_file is not None:
            with st.spinner("🔄 AI is working its magic... This may take a few moments."):
                result_image = process_images(person_image, clothing_image, clothing_type, style_details)
                
                if result_image:
                    st.success("✅ Image generated successfully!")
                    
                    # Display result
                    st.subheader("🎉 Result")
                    st.image(result_image, caption="Generated Image", use_column_width=True)
                    
                    # Download button
                    buf = BytesIO()
                    result_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="📥 Download Generated Image",
                        data=byte_im,
                        file_name="ai_clothing_replacement.png",
                        mime="image/png",
                        use_container_width=True
                    )
        else:
            st.warning("⚠️ Please upload both images before generating!")
    
    # Example section
    with st.expander("📋 How to use this tool"):
        st.markdown("""
        1. **Upload Person's Photo**: Choose a clear image of a person wearing clothes you want to replace
        2. **Upload Clothing Item**: Choose an image of the clothing item you want the person to wear
        3. **Select Clothing Type**: Choose the appropriate clothing category from the sidebar
        4. **Add Style Instructions** (Optional): Provide specific instructions for better results
        5. **Generate**: Click the generate button and wait for the AI to create the new image
        
        **Tips for best results:**
        - Use high-quality, well-lit images
        - Ensure the person is clearly visible in the photo
        - Choose clothing items with clear details and good contrast
        - Provide specific style instructions if needed
        """)

    # Footer
    st.markdown("---")
    st.markdown("### 📧 Contact Information")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("**Email:** contact@yashddesai.com")
        st.markdown("**Website:** [yashddesai.com](https://yashddesai.com)")
        st.markdown("")
        st.markdown("💡 **Loved this AI try-on feature?**")
        st.markdown("I'm passionate about creating innovative AI solutions. If you'd like to implement this technology in your own application or explore custom AI development services, I'd be delighted to discuss how we can bring your vision to life.")
        st.markdown("")
        st.markdown("📩 **Get in touch** and let's create something amazing together!")

if __name__ == "__main__":
    main()