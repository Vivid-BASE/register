
import sys

file_path = '/Volumes/Untitled/AI/register/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update applyProductTemplate
old_template = """        function applyProductTemplate(type) {
            if (!type) return;

            const nameInput = document.getElementById('newProdName');
            const container = document.getElementById('newProdVariants');
            container.innerHTML = ''; // Clear existing

            // Auto-set Icon if possible (optional refinement)
            // nameInput.value could be set too

            let variants = [];

            if (type === 'tshirt') {
                nameInput.value = 'Tシャツ';
                variants = ['S', 'M', 'L', 'XL'];
            } else if (type === 'longT') {
                nameInput.value = 'ロンT';
                variants = ['S', 'M', 'L', 'XL'];
            } else if (type === 'towel') {
                nameInput.value = 'フェイスタオル';
                // Single generic variant or color
                addVariantRow('newProdVariants', { name: 'Free', price: '', stock: '' });
                return;
            } else if (type === 'muffler') {
                nameInput.value = 'マフラータオル';
                variants = ['赤', '青'];
            } else if (type === 'cheki') {
                nameInput.value = 'チェキ';
                addVariantRow('newProdVariants', { name: 'Normal', price: '1000', stock: '' });
                addVariantRow('newProdVariants', { name: 'Sign', price: '2000', stock: '' });
                return;
            } else if (type === 'adult') {
                // Keep backward compatibility for presets logic if needed, but UI replaced
                variants = ['S', 'M', 'L', 'XL'];
            }

            variants.forEach(v => {
                addVariantRow('newProdVariants', { name: v, price: '', stock: '' });
            });

            // Reset select?
            // document.getElementById('productTemplateSelect').value = ''; 
        }"""

new_template = """        function applyProductTemplate(type) {
            if (!type) return;

            const nameInput = document.getElementById('newProdName');
            const container = document.getElementById('newProdVariants');
            container.innerHTML = ''; // Clear existing

            let variants = [];
            const freeVal = t('freeSize');
            const signVal = t('signed');
            const normalVal = t('normal');

            if (type === 'tshirt') {
                nameInput.value = t('tshirt');
                variants = [t('sizeS'), t('sizeM'), t('sizeL'), t('sizeXL')];
            } else if (type === 'longT') {
                nameInput.value = t('longT');
                variants = [t('sizeS'), t('sizeM'), t('sizeL'), t('sizeXL')];
            } else if (type === 'towel') {
                nameInput.value = t('towel');
                addVariantRow('newProdVariants', { name: freeVal, price: '', stock: '' });
                return;
            } else if (type === 'muffler') {
                nameInput.value = t('muffler');
                variants = [t('red'), t('blue')];
            } else if (type === 'cheki') {
                nameInput.value = t('cheki');
                addVariantRow('newProdVariants', { name: normalVal, price: '1000', stock: '' });
                addVariantRow('newProdVariants', { name: signVal, price: '2000', stock: '' });
                return;
            } else if (type === 'adult') {
                variants = [t('sizeS'), t('sizeM'), t('sizeL'), t('sizeXL')];
            }

            variants.forEach(v => {
                addVariantRow('newProdVariants', { name: v, price: '', stock: '' });
            });
        }"""

if old_template in content:
    content = content.replace(old_template, new_template)
else:
    print("Could not find old_template")
    sys.exit(1)

# 2. Update renderSettingsList
# We'll use a more robust regex or split/join for this if needed, but let's try direct replacement of the inner parts.

old_settings_start = "        function renderSettingsList() {"
old_settings_end = "            renderExistingProducts();\n        }"

# Find the start and end indices
start_idx = content.find(old_settings_start)
end_idx = content.find(old_settings_end, start_idx)

if start_idx != -1 and end_idx != -1:
    end_idx += len(old_settings_end)
    new_settings_func = """        function renderSettingsList() {
            const container = document.getElementById('settingsList');
            
            const productKeys = [
                'tshirt', 'longT', 'towel', 'muffler', 'cheki', 'sticker', 'hoodie', 'tote', 
                'acrylic', 'keyholder', 'postcard', 'pamphlet', 'cd', 'dvd', 'bluray', 
                'calendar', 'photobook', 'penlight', 'wristband'
            ];
            const variantKeys = [
                'sizeS', 'sizeM', 'sizeL', 'sizeXL', 'sizeXS', 'sizeXXL', 'freeSize', 
                'ladies', 'red', 'blue', 'yellow', 'green', 'white', 'black', 'normal', 
                'signed', 'set'
            ];

            container.innerHTML = `
                <div class="settings-container">
                    <div id="pwa-settings-guide" class="setting-item" style="background:rgba(0,123,255,0.05); border:1px dashed var(--primary-color);">
                        <i class="fas fa-mobile-alt"></i>
                        <div style="flex:1; font-size:0.85rem;">
                            <strong data-i18n="pwaBannerTitle">ホーム画面に追加して使う</strong><br>
                            <span style="color:#666; font-size:0.75rem;" data-i18n="pwaBannerDesc">全画面表示になり、より本物のレジのように使いやすくなります。</span>
                        </div>
                        <button onclick="showInstallBanner(true)" style="background:var(--primary-color); color:#fff; border:none; padding:5px 12px; border-radius:6px; font-size:0.75rem; cursor:pointer;" data-i18n="pwaGuideBtn">ガイドを表示</button>
                    </div>

                    <!-- Global Settings Card -->
                    <div class="settings-card">
                        <h3 data-i18n="globalSettings">全体設定</h3>
                        <div class="form-group">
                            <label data-i18n="displayLanguage">表示言語</label>
                            <select class="form-control" onchange="changeLanguage(this.value)">
                                <option value="ja" ${currentLanguage === 'ja' ? 'selected' : ''}>日本語</option>
                                <option value="en" ${currentLanguage === 'en' ? 'selected' : ''}>English</option>
                                <option value="zh" ${currentLanguage === 'zh' ? 'selected' : ''}>中国語 (簡体字)</option>
                                <option value="tw" ${currentLanguage === 'tw' ? 'selected' : ''}>中国語 (繁体字)</option>
                                <option value="es" ${currentLanguage === 'es' ? 'selected' : ''}>Español</option>
                                <option value="fr" ${currentLanguage === 'fr' ? 'selected' : ''}>Français</option>
                                <option value="de" ${currentLanguage === 'de' ? 'selected' : ''}>Deutsch</option>
                                <option value="pt" ${currentLanguage === 'pt' ? 'selected' : ''}>Português</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label data-i18n="currencyRegion">通貨・地域</label>
                            <select class="form-control" onchange="changeRegion(this.value)">
                                <option value="ja" ${currentRegion === 'ja' ? 'selected' : ''}>日本 (¥ / amazon.co.jp)</option>
                                <option value="en" ${currentRegion === 'en' ? 'selected' : ''}>US ($ / amazon.com)</option>
                                <option value="zh" ${currentRegion === 'zh' ? 'selected' : ''}>China (¥ / amazon.cn)</option>
                                <option value="tw" ${currentRegion === 'tw' ? 'selected' : ''}>Taiwan ($ / amazon.com)</option>
                                <option value="es" ${currentRegion === 'es' ? 'selected' : ''}>Spain (€ / amazon.es)</option>
                                <option value="fr" ${currentRegion === 'fr' ? 'selected' : ''}>France (€ / amazon.fr)</option>
                                <option value="de" ${currentRegion === 'de' ? 'selected' : ''}>Germany (€ / amazon.de)</option>
                                <option value="pt" ${currentRegion === 'pt' ? 'selected' : ''}>Portugal (€ / amazon.pt)</option>
                            </select>
                        </div>
                    </div>
                    <!-- New Product Form -->
                    <div class="settings-card">
                        <h3 data-i18n="addProductTitle">商品を登録する</h3>
                        <div class="form-group">
                            <label data-i18n="productNameLabel">商品名</label>
                            <input type="text" id="newProdName" class="form-control" placeholder="例: Tシャツ" list="commonProductNames">
                            <datalist id="commonProductNames">
                                ${productKeys.map(k => `<option value="${t(k)}">`).join('')}
                            </datalist>
                        </div>
                        <div class="form-group">
                            <label data-i18n="variantsLabel">バリエーション (サイズ/色)</label>
                            <datalist id="commonVariantNames">
                                ${variantKeys.map(k => `<option value="${t(k)}">`).join('')}
                            </datalist>
                            <div id="newProdVariants"></div>
                            <button class="btn-add-variant" onclick="addVariantRow('newProdVariants')">＋ ${t('variantLabel')}</button>
                        </div>
                        <button class="btn-save-product" onclick="saveNewProduct()" data-i18n="saveButton">保存する</button>
                    </div>

                    <!-- Existing Products List -->
                    <div class="settings-card">
                        <h3 data-i18n="registeredProductsTitle">登録済み商品一覧</h3>
                        <div id="existingProductsList"></div>
                    </div>

                    <!-- App Info Footer -->
                    <div style="margin-top: 40px; text-align: center; color: #999; font-size: 0.8rem; padding-bottom: 20px;">
                        <button onclick="manualUpdateCheck()" style="padding: 10px 20px; background: #fff; border: 1px solid #ccc; border-radius: 8px; font-weight: bold; color: #333; margin-bottom: 20px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.05);" data-i18n="updateNow">
                            🔄 最新バージョンを確認
                        </button>
                        <p>BOXXレジ App v3.0.0</p>
                        <p>Developed by <a href="https://showtimeboxx.com/lab/?utm_source=boxx_regi_app&utm_medium=footer_link" target="_blank" style="color:#999; text-decoration:none;">SHOWTIMEBOXX LAB</a></p>
                    </div>
                </div>
            `;

            applyTranslations(); 
            addVariantRow('newProdVariants');
            renderExistingProducts();
        }"""
    content = content[:start_idx] + new_settings_func + content[end_idx:]
else:
    print(f"Could not find renderSettingsList boundaries: start={start_idx}, end={end_idx}")
    sys.exit(1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated index.html")
