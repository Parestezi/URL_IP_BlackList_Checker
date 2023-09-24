# URL ve IP Adresi İzleme Uygulaması

Bu Python tabanlı uygulama, verilen URL'leri ve IP adreslerini izlemek, güvenlik durumlarını kontrol etmek ve değişiklikleri izlemek için kullanılır. Ayrıca Google Safe Browsing API'yi kullanarak kötü niyetli URL'leri belirlemek için asenkron bir işlev içerir.

## Başlarken

Bu uygulamayı yerel bir ortamda çalıştırmak ve bağımlılıkları yönetmek için Poetry kullanıyoruz.

### Gereksinimler

- Python 3.x
- Poetry (Proje bağımlılıklarını yönetmek için)
- Google Safe Browsing API Anahtarı (Kötü niyetli URL taraması için gereklidir)

### Kurulum

1. Bu depoyu yerel bilgisayarınıza klonlayın.

   ```markdown
   git clone https://github.com/Parestezi/URL_IP_BlackList_Checker

2. Proje dizinine gidin.
   ```markdown
   cd URL_IP_BlackList_Checker

3. Poetry ile projeyi yükleyin ve bağımlılıkları kurun.
   ```markdown
   poetry install

4. .env dosyasını oluşturun ve Google Safe Browsing API Anahtarınızı ekleyin.
      ```markdown
      GOOGLE_SAFE_BROWSING_API_KEY=your_api_key_here

### Kullanım
Uygulamayı başlattıktan sonra, bir dosyanın adını gireceğiniz bir istem alırsınız. Bu dosya, izlemek istediğiniz URL'leri veya IP adreslerini içermelidir.

Dosya içeriğini okur ve veritabanına URL'leri veya IP adreslerini ekler.

Uygulama, belirli aralıklarla URL'leri veya IP adreslerini kontrol eder ve güvenlik durumunu kontrol eder.

Kötü niyetli bir URL tespit edildiğinde, ilgili giriş "Yes" olarak güncellenir.

Down veya Redirection durumları tespit edildiğinde, bu URL'ler "down_redirection_urls.txt" dosyasına kaydedilir.
