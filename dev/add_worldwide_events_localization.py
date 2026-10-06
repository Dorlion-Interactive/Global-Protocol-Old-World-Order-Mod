import os
import glob

# 12 keys across 3 worldwide historical narrative events:
# - tumu_crisis_beijing_1450 (MYN)
# - rise_of_tawantinsuyu_1450 (INC)
# - songhai_ascendancy_1464 (SON)

L10N_DATA = {
    "en": {
        "owo.event.tumu_crisis_beijing_1450.title": "The Tumu Crisis and Defense of Beijing",
        "owo.event.tumu_crisis_beijing_1450.description": "Following the disastrous capture of Emperor Zhengtong by the Oirat Mongols at Tumu, the enemy host has advanced to the gates of Beijing. Minister of War Yu Qian has enthroned the Jingtai Emperor and rallied the imperial garrison, mounting heavy artillery and fire-lances along the capital's battlements to break the northern siege.",
        "owo.event.tumu_crisis_beijing_1450.option_1": "Rally under Yu Qian; not an inch of the capital shall yield!",
        "owo.event.tumu_crisis_beijing_1450.option_2": "Offer silver and silks to negotiate an immediate northern truce.",

        "owo.event.rise_of_tawantinsuyu_1450.title": "Pachacuti and the Rise of Tawantinsuyu",
        "owo.event.rise_of_tawantinsuyu_1450.description": "Having defended Cusco against the ferocious Chanca invasion, Sapa Inca Pachacuti Yupanqui has proclaimed the founding of Tawantinsuyu—the Realm of the Four Parts. Ordering the rebuilding of Cusco with monumental stonework and terracing the Andean slopes, Pachacuti marches to unify the mountain valleys under the mantle of the Sun God Inti.",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "Proclaim Tawantinsuyu and march across the Andes!",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "Consolidate the Sacred Valley and enrich the Coricancha.",

        "owo.event.songhai_ascendancy_1464.title": "Sunni Ali and the Songhai Ascendancy",
        "owo.event.songhai_ascendancy_1464.description": "Ascending the throne of Gao in 1464, Sunni Ali Ber has transformed the Songhai kingdom into an unstoppable imperial force. Commanding an armada of war canoes along the Niger River and swift armored cavalry across the Sahel, Sunni Ali prepares to liberate Timbuktu from the Tuareg and seize dominion over the lucrative trans-Saharan trade routes.",
        "owo.event.songhai_ascendancy_1464.option_1": "Launch the Niger river fleet and claim the Sahel!",
        "owo.event.songhai_ascendancy_1464.option_2": "Guard the gates of Gao and trade peacefully along the river."
    },
    "tr": {
        "owo.event.tumu_crisis_beijing_1450.title": "Tumu Krizi ve Pekin Savunması",
        "owo.event.tumu_crisis_beijing_1450.description": "İmparator Zhengtong'un Tumu'da Oyrat Moğolları tarafından esir alınmasının ardından düşman ordusu Pekin surlarına dayandı. Savaş Bakanı Yu Qian, Jingtai İmparatoru'nu tahta çıkararak başkenti savundu; surlara ateş mızrakları ve ağır toplar yerleştirerek kuzey kuşatmasını püskürttü.",
        "owo.event.tumu_crisis_beijing_1450.option_1": "Yu Qian önderliğinde direnin; başkentten bir karış toprak verilmeyecek!",
        "owo.event.tumu_crisis_beijing_1450.option_2": "Kuzeyle ateşkes için gümüş ve ipek haraç teklif et.",

        "owo.event.rise_of_tawantinsuyu_1450.title": "Pachacuti ve Tawantinsuyu'nun Yükselişi",
        "owo.event.rise_of_tawantinsuyu_1450.description": "Cusco'yu Chanca istilasına karşı başarıyla savunan Sapa İnka Pachacuti Yupanqui, Tawantinsuyu'nun (Dört Bölgenin Diyarı) kuruluşunu ilan etti. Cusco'yu anıtsal taş yapılarla yeniden inşa ettirip And yamaçlarını teraslayan Pachacuti, dağ vadilerini Güneş Tanrısı İnti sancağı altında birleştirmek üzere sefere çıkıyor.",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "Tawantinsuyu'yu ilan et ve And Dağları'nda sefere çık!",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "Kutsal Vadi'yi tahkim et ve Coricancha tapınağını zenginleştir.",

        "owo.event.songhai_ascendancy_1464.title": "Sonni Ali ve Songhay Yükselişi",
        "owo.event.songhai_ascendancy_1464.description": "1464'te Gao tahtına çıkan Sonni Ali Ber, Songhay krallığını durdurulamaz bir imparatorluğa dönüştürdü. Nijer Nehri üzerindeki savaş kanoları filosu ve Sahel'deki zırhlı süvarileriyle Sonni Ali, Timbuktu'yu Tuareglerden alarak Sahra ötesi altın ve tuz ticaret yollarını ele geçirmeye hazırlanıyor.",
        "owo.event.songhai_ascendancy_1464.option_1": "Nijer donanmasını sefere çıkar ve Sahel'e hükmet!",
        "owo.event.songhai_ascendancy_1464.option_2": "Gao kapılarını koru ve nehir boyunca barış içinde ticaret yap."
    },
    "de": {
        "owo.event.tumu_crisis_beijing_1450.title": "Die Tumu-Krise und Verteidigung von Peking",
        "owo.event.tumu_crisis_beijing_1450.description": "Nach der Gefangennahme des Zhengtong-Kaisers durch die Oiraten bei Tumu rückten die Mongolen vor die Tore Pekings vor. Kriegsminister Yu Qian krönte den Jingtai-Kaiser und verteidigte die Hauptstadt mit Kanonen und Feuerlanzen erfolgreich gegen die Belagerung.",
        "owo.event.tumu_crisis_beijing_1450.option_1": "Peking unter Yu Qian verteidigen; keinen Fußbreit weichen!",
        "owo.event.tumu_crisis_beijing_1450.option_2": "Silber und Seide bieten, um einen Waffenstillstand zu erkaufen.",

        "owo.event.rise_of_tawantinsuyu_1450.title": "Pachacuti und der Aufstieg von Tawantinsuyu",
        "owo.event.rise_of_tawantinsuyu_1450.description": "Nach der Abwehr der Chanca gründete Sapa Inka Pachacuti Yupanqui das Reich Tawantinsuyu. Er baute Cusco mit monumentalen Steinbauten aus und marschierte aus, um die Anden unter dem Sonnengott Inti zu vereinen.",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "Tawantinsuyu ausrufen und die Anden erobern!",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "Das Heilige Tal stärken und den Coricancha-Tempel bereichern.",

        "owo.event.songhai_ascendancy_1464.title": "Sunni Ali und der Aufstieg des Songhai-Reiches",
        "owo.event.songhai_ascendancy_1464.description": "1464 bestieg Sunni Ali Ber den Thron von Gao und machte Songhai zur führenden Macht Westafrikas. Mit einer Kriegsflotte auf dem Niger und Reitertruppen eroberte er Timbuktu und die Transsahara-Handelsrouten.",
        "owo.event.songhai_ascendancy_1464.option_1": "Die Flussflotte entsenden und den Sahel beherrschen!",
        "owo.event.songhai_ascendancy_1464.option_2": "Gao schützen und friedlichen Handel am Niger treiben."
    },
    "fr": {
        "owo.event.tumu_crisis_beijing_1450.title": "La Crise de Tumu et la Défense de Pékin",
        "owo.event.tumu_crisis_beijing_1450.description": "Après la capture de l'empereur Zhengtong à Tumu par les Oïrats, les Mongols assiègent Pékin. Le ministre de la guerre Yu Qian intronise l'empereur Jingtai et repousse victorieusement le siège à coups de canons et de lances à feu.",
        "owo.event.tumu_crisis_beijing_1450.option_1": "Défendre Pékin sous les ordres de Yu Qian; ne rien céder !",
        "owo.event.tumu_crisis_beijing_1450.option_2": "Offrir tribut d'argent et de soie pour négocier une trêve.",

        "owo.event.rise_of_tawantinsuyu_1450.title": "Pachacuti et l'Essor du Tawantinsuyu",
        "owo.event.rise_of_tawantinsuyu_1450.description": "Après avoir sauvé Cuzco des Chancas, le Sapa Inca Pachacuti proclame l'empire du Tawantinsuyu. Il rebâtit Cuzco en pierre de taille et entreprend d'unifier les Andes sous l'égide du dieu Soleil Inti.",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "Proclamer le Tawantinsuyu et conquérir les Andes !",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "Embellir la Vallée Sacrée et le temple du Coricancha.",

        "owo.event.songhai_ascendancy_1464.title": "Sonni Ali et l'Ascension Songhaï",
        "owo.event.songhai_ascendancy_1464.description": "Couronné à Gao en 1464, Sonni Ali Ber transforme le royaume songhaï en un puissant empire. Disposant d'une flotte de pirogues sur le Niger et d'une cavalerie redoutable, il s'empare de Tombouctou et des routes transsahariennes.",
        "owo.event.songhai_ascendancy_1464.option_1": "Mobiliser la flotte du Niger et dominer le Sahel !",
        "owo.event.songhai_ascendancy_1464.option_2": "Fortifier Gao et commercer en paix le long du fleuve."
    },
    "es": {
        "owo.event.tumu_crisis_beijing_1450.title": "La Crisis de Tumu y la Defensa de Pekín",
        "owo.event.tumu_crisis_beijing_1450.description": "Tras la captura del emperador Zhengtong en Tumu por los oirates, los mongoles sitiaron Pekín. El ministro de guerra Yu Qian proclamó al emperador Jingtai y repelió el asedio con artillería pesada y lanzas de fuego.",
        "owo.event.tumu_crisis_beijing_1450.option_1": "¡Defender Pekín bajo el mando de Yu Qian; ni un palmo al invasor!",
        "owo.event.tumu_crisis_beijing_1450.option_2": "Ofrecer tributo de plata y seda para pactar una tregua.",

        "owo.event.rise_of_tawantinsuyu_1450.title": "Pachacútec y el Surgimiento del Tawantinsuyu",
        "owo.event.rise_of_tawantinsuyu_1450.description": "Tras vencer a los chancas en el Cusco, el Sapa Inca Pachacútec proclamó la fundación del Tawantinsuyu, las Cuatro Regiones. Reconstruyendo el Cusco en piedra pulida y terrazas andinas, marcha para unificar los Andes bajo el dios Inti.",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "¡Proclamar el Tawantinsuyu y marchar por los Andes!",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "Consolidar el Valle Sagrado y enriquecer el Coricancha.",

        "owo.event.songhai_ascendancy_1464.title": "Sonni Alí y la Hegemonía Songhai",
        "owo.event.songhai_ascendancy_1464.description": "Al asumir el trono de Gao en 1464, Sonni Alí Ber convirtió al reino Songhai en un imperio dominante en África occidental. Con canoas de guerra en el río Níger y caballería en el Sahel, toma Tombuctú y domina las rutas transaharianas.",
        "owo.event.songhai_ascendancy_1464.option_1": "¡Desplegar la flota del río Níger y dominar el Sahel!",
        "owo.event.songhai_ascendancy_1464.option_2": "Proteger Gao y mantener el comercio fluvial pacífico."
    },
    "zh": {
        "owo.event.tumu_crisis_beijing_1450.title": "土木堡之变与北京保卫战",
        "owo.event.tumu_crisis_beijing_1450.description": "土木堡之变明英宗蒙尘瓦剌，也先大军直逼京师九门。兵部尚书于谦力排南迁之议，拥立景泰帝，调集勤王军民于城下架设大炮火铳、神机铳矢，决死击退瓦剌铁骑，力挽狂澜！",
        "owo.event.tumu_crisis_beijing_1450.option_1": "社稷为重！听于谦号令死守京师，寸土不让！",
        "owo.event.tumu_crisis_beijing_1450.option_2": "犒赏金银绸缎，暂缓北方战事求得停战。",

        "owo.event.rise_of_tawantinsuyu_1450.title": "帕查库蒂与印加帝国的兴起",
        "owo.event.rise_of_tawantinsuyu_1450.description": "击溃昌卡人进犯后，萨帕·印加帕查库蒂宣布建立塔万廷苏尤（四方之地）。他以巨石重修库斯科圣城，开辟安第斯梯田水渠，率军出征，将太阳神因蒂的荣耀普照群山。",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "建立四方帝国，挥师征战安第斯诸部！",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "营建圣谷梯田，修葺太阳神殿柯里坎查。",

        "owo.event.songhai_ascendancy_1464.title": "桑尼·阿里与桑海帝国的崛起",
        "owo.event.songhai_ascendancy_1464.description": "1464年桑尼·阿里即位于加奥，迅速将桑海推向帝国鼎盛。凭借尼日尔河上的战船舰队与萨赫勒重骑兵，桑海大军进逼廷巴克图，掌控跨撒哈拉黄金与食盐贸易商道。",
        "owo.event.songhai_ascendancy_1464.option_1": "调集尼日尔水师与骑兵，横扫萨赫勒！",
        "owo.event.songhai_ascendancy_1464.option_2": "镇守加奥重镇，维系沿河商旅往来。"
    },
    "ru": {
        "owo.event.tumu_crisis_beijing_1450.title": "Тумуская катастрофа и оборона Пекина",
        "owo.event.tumu_crisis_beijing_1450.description": "После пленения императора ойратами при Туму монголы подошли к Пекину. Военный министр Юй Цянь посадил на трон императора Цзинтая и отстоял столицу, сокрушив врага артиллерией со стен города.",
        "owo.event.tumu_crisis_beijing_1450.option_1": "Защищать столицу под началом Юй Цяня до последнего!",
        "owo.event.tumu_crisis_beijing_1450.option_2": "Отправить серебро и шелка ради перемирия.",

        "owo.event.rise_of_tawantinsuyu_1450.title": "Пачакутек и рождение Тауантинсуйу",
        "owo.event.rise_of_tawantinsuyu_1450.description": "Разгромив племя чанка, Сапа Инка Пачакутек провозгласил создание империи Тауантинсуйу. Перестроив Куско из камня и возведя террасы в Андах, он начал объединение горных долин под знаменем бога Инти.",
        "owo.event.rise_of_tawantinsuyu_1450.option_1": "Провозгласить Тауантинсуйу и начать поход по Андам!",
        "owo.event.rise_of_tawantinsuyu_1450.option_2": "Укрепить Священную долину и храм Кориканча.",

        "owo.event.songhai_ascendancy_1464.title": "Сонни Али и возвышение Сонгай",
        "owo.event.songhai_ascendancy_1464.description": "Взойдя на престол Гао в 1464 году, Сонни Али Бер превратил царство Сонгай в могущественную империю. Располагая флотом боевых пирог на реке Нигер и кавалерией, он подчинил Тимбукту и транссахарские пути.",
        "owo.event.songhai_ascendancy_1464.option_1": "Спустить флот на реку Нигер и покорить Сахель!",
        "owo.event.songhai_ascendancy_1464.option_2": "Защищать Гао и развивать торговлю на реке."
    }
}

# Regional fallbacks
LANG_MAP = {
    "es-419": "es",
    "pt": "es",
    "pt-br": "es",
    "cz": "de",
    "ja": "zh",
    "ko": "zh"
}

all_langs = ["cz", "de", "en", "es", "es-419", "fr", "ja", "ko", "pt", "pt-br", "ru", "tr", "zh"]

def run():
    for lang in all_langs:
        filepath = f"Content/localization/{lang}.csv"
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        existing_keys = {line.split(",")[0].strip() for line in lines if "," in line}

        src_lang = lang if lang in L10N_DATA else LANG_MAP.get(lang, "en")
        dict_to_use = L10N_DATA.get(src_lang, L10N_DATA["en"])

        new_lines = []
        for key, val in dict_to_use.items():
            if key not in existing_keys:
                # Clean line breaks or commas if any
                clean_val = val.replace("\n", " ").replace("\r", "")
                new_lines.append(f"{key},{clean_val}\n")

        if new_lines:
            with open(filepath, "a", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"Added {len(new_lines)} keys to {filepath}")
        else:
            print(f"No new keys needed for {filepath}")

if __name__ == "__main__":
    run()
