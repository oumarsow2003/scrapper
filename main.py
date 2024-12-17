import os
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


def vote_instance(proxy):
    """Exécute une instance de vote de manière infinie."""
    with sync_playwright() as p:
        while True:
            try:
                # Configurer le navigateur
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Accéder au site et effectuer les actions
                page.goto("https://lesvdmg.com/")
                page.locator(
                    "#totalpoll-poll-4781 > .totalpoll-form > .totalpoll-questions > .totalpoll-question > .totalpoll-question-container > .totalpoll-question-choices > label:nth-child(2) > .totalpoll-question-choices-item-container > .totalpoll-question-choices-item-control > .totalpoll-question-choices-item-selector > .totalpoll-question-choices-item-selector-box").click()
                page.locator("#totalpoll-poll-4781").get_by_role("button", name="Vote").click()

                # Pause entre les itérations pour éviter de surcharger le serveur
                page.wait_for_timeout(1200)
            except Exception as e:
                print(f"Erreur dans une ins <tance : {e}")
            finally:
                # Assurez-vous que le navigateur est fermé même en cas d'erreur
                browser.close()


def main():
    proxy = os.environ["PROXY"]
    num_instances = 15 # Nombre d'instances simultanées

    # Lancer les threads pour exécuter des tâches infinies
    with ThreadPoolExecutor(max_workers=num_instances) as executor:
        # Chaque thread exécute vote_instance() avec le proxy donné
        for _ in range(num_instances):
            executor.submit(vote_instance, proxy)

    # Garder le programme principal actif
    try:
        while True:
            pass  # Boucle infinie pour maintenir le programme en vie
    except KeyboardInterrupt:
        print("Programme arrêté manuellement.")


if __name__ == "__main__":
    main()
