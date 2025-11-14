# backend/test_connexion.py
import pymysql
import sys

def test_connexion_wamp():
    print("🧪 TEST DE CONNEXION WAMP MySQL")
    print("=" * 40)
    
    try:
        print("🔗 Tentative de connexion à MySQL...")
        print("📍 Host: localhost")
        print("👤 User: root") 
        print("📊 Database: assistant_revisions")
        
        # Connexion avec PyMySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='assistant_revisions',
            port=3306,
            charset='utf8mb4'
        )
        
        print("✅ CONNEXION RÉUSSIE !")
        
        # Test des tables
        cursor = connection.cursor()
        
        # 1. Vérifier les tables
        print("\n📋 VÉRIFICATION DES TABLES...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ {len(tables)} table(s) trouvée(s):")
            for table in tables:
                print(f"   • {table[0]}")
        else:
            print("❌ Aucune table trouvée")
            
        # 2. Vérifier la structure des tables principales
        print("\n🔍 STRUCTURE DES TABLES:")
        tables_to_check = ['users', 'modules', 'quizzes', 'scores', 'study_plans']
        
        for table_name in tables_to_check:
            try:
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print(f"\n📊 Table '{table_name}':")
                for col in columns:
                    print(f"   └ {col[0]} ({col[1]})")
            except Exception as e:
                print(f"❌ Table '{table_name}' non trouvée")
        
        # 3. Test simple de comptage
        print("\n🧪 TEST SIMPLE...")
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"👥 Nombre d'utilisateurs: {user_count}")
        except:
            print("👥 Aucun utilisateur (c'est normal pour l'instant)")
        
        cursor.close()
        connection.close()
        print("\n🔌 Connexion fermée")
        print("🎉 TEST RÉUSSI ! La base est prête.")
        
    except pymysql.Error as e:
        print(f"\n❌ ERREUR MySQL: {e}")
        print("\n🔧 DIAGNOSTIC:")
        
        error_msg = str(e)
        if "Unknown database" in error_msg:
            print("   • La base 'assistant_revisions' n'existe pas")
            print("   • Créez-la dans phpMyAdmin")
            
        elif "Access denied" in error_msg:
            print("   • Problème d'authentification")
            print("   • Vérifiez user/mot de passe WAMP")
            
        elif "Can't connect" in error_msg:
            print("   • WAMP n'est pas démarré")
            print("   • Vérifiez que l'icône WAMP est VERTE")
            
        else:
            print(f"   • Erreur: {e}")
            
    except Exception as e:
        print(f"\n❌ ERREUR générale: {e}")
        print(f"   Type: {type(e).__name__}")

if __name__ == "__main__":
    test_connexion_wamp()
    input("\nAppuyez sur Entrée pour fermer...")