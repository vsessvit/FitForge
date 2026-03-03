module.exports = {
    languageOptions: {
        ecmaVersion: 2018,
        sourceType: 'script',
        globals: {
            browser: true,
            jquery: true,
            Stripe: 'readonly',
            $: 'readonly',
            jQuery: 'readonly'
        }
    },
    rules: {
        'indent': ['error', 4],
        'quotes': ['error', 'single'],
        'semi': ['error', 'always'],
        'no-unused-vars': ['warn'],
        'no-console': 'off'
    }
};
