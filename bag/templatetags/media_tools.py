from django import template

register = template.Library()


CLOUDINARY_PRESETS = {
    'class_card': 'f_auto,q_auto,dpr_auto,c_fill,w_640,h_360',
    'class_detail': 'f_auto,q_auto,dpr_auto,c_fill,w_960,h_640',
    'product_card': 'f_auto,q_auto,dpr_auto,c_fill,w_640,h_640',
    'product_detail': 'f_auto,q_auto,dpr_auto,c_fill,w_1000,h_1000',
}


@register.filter(name='cld_optimize')
def cld_optimize(image_url, preset=''):
    """Apply Cloudinary transformation presets when possible.

    Usage in templates:
        {{ image.url|cld_optimize:'product_card' }}
    """
    if not image_url:
        return image_url

    url = str(image_url)

    if 'res.cloudinary.com' not in url or '/image/upload/' not in url:
        return url

    if '/image/upload/f_auto' in url:
        return url

    transformation = CLOUDINARY_PRESETS.get(
        preset,
        'f_auto,q_auto,dpr_auto',
    )

    prefix, suffix = url.split('/image/upload/', 1)
    return f'{prefix}/image/upload/{transformation}/{suffix}'
