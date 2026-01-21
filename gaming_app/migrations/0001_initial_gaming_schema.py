"""
Migration to create gaming schema and tables
Run this migration after creating the schema in PostgreSQL
"""
from django.db import migrations


def create_gaming_schema(apps, schema_editor):
    """Create gaming schema and tables"""
    with schema_editor.connection.cursor() as cursor:
        # Create schema
        cursor.execute("CREATE SCHEMA IF NOT EXISTS gaming;")
        cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA gaming TO CURRENT_USER;")
        
        # Create level table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gaming.level (
                id SERIAL PRIMARY KEY,
                code VARCHAR(100) NOT NULL,
                "order" INTEGER NOT NULL UNIQUE,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                requiredpoints INTEGER NOT NULL,
                icon VARCHAR(255),
                companyid INTEGER,
                isactive BOOLEAN DEFAULT TRUE
            );
        """)
        
        # Create indexes for level
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_level_companyId ON gaming.level(companyid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_level_code ON gaming.level(code);")
        
        # Create userlevel table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gaming.userlevel (
                id SERIAL PRIMARY KEY,
                userid INTEGER NOT NULL,
                levelid INTEGER NOT NULL,
                currentpoints INTEGER DEFAULT 0,
                reachedat TIMESTAMP NOT NULL,
                UNIQUE(userid, levelid)
            );
        """)
        
        # Create indexes for userlevel
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userLevel_userId ON gaming.userlevel(userid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userLevel_levelId ON gaming.userlevel(levelid);")
        
        # Create badge table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gaming.badge (
                id SERIAL PRIMARY KEY,
                code VARCHAR(100) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                icon VARCHAR(255),
                missionid INTEGER,
                companyid INTEGER,
                isactive BOOLEAN DEFAULT TRUE
            );
        """)
        
        # Create indexes for badge
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_badge_companyId ON gaming.badge(companyid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_badge_missionId ON gaming.badge(missionid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_badge_code ON gaming.badge(code);")
        
        # Create userbadge table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gaming.userbadge (
                id SERIAL PRIMARY KEY,
                userid INTEGER NOT NULL,
                badgeid INTEGER NOT NULL,
                earnedat TIMESTAMP NOT NULL,
                UNIQUE(userid, badgeid)
            );
        """)
        
        # Create indexes for userbadge
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userBadge_userId ON gaming.userbadge(userid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userBadge_badgeId ON gaming.userbadge(badgeid);")
        
        # Create userpoint table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gaming.userpoint (
                id SERIAL PRIMARY KEY,
                userid INTEGER NOT NULL UNIQUE,
                totalpoints INTEGER DEFAULT 0,
                lastupdated TIMESTAMP
            );
        """)
        
        # Create indexes for userpoint
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userPoint_userId ON gaming.userpoint(userid);")
        
        # Create useraction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gaming.useraction (
                id SERIAL PRIMARY KEY,
                userid INTEGER NOT NULL,
                actiontype VARCHAR(100) NOT NULL,
                pointsearned INTEGER DEFAULT 0,
                description TEXT,
                createdat TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes for useraction
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userAction_userId ON gaming.useraction(userid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userAction_actionType ON gaming.useraction(actiontype);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_userAction_createdAt ON gaming.useraction(createdat);")
        
        # Foreign Key Constraints
        # Level foreign keys
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.level 
                ADD CONSTRAINT fk_level_companyId 
                FOREIGN KEY (companyid) REFERENCES users.company(id) ON DELETE SET NULL;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # UserLevel foreign keys
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.userlevel 
                ADD CONSTRAINT fk_userLevel_userId 
                FOREIGN KEY (userid) REFERENCES users.user(id) ON DELETE CASCADE;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.userlevel 
                ADD CONSTRAINT fk_userLevel_levelId 
                FOREIGN KEY (levelid) REFERENCES gaming.level(id) ON DELETE CASCADE;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # Badge foreign keys
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.badge 
                ADD CONSTRAINT fk_badge_companyId 
                FOREIGN KEY (companyid) REFERENCES users.company(id) ON DELETE SET NULL;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.badge 
                ADD CONSTRAINT fk_badge_missionId 
                FOREIGN KEY (missionid) REFERENCES roadmap.mission(id) ON DELETE SET NULL;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # UserBadge foreign keys
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.userbadge 
                ADD CONSTRAINT fk_userBadge_userId 
                FOREIGN KEY (userid) REFERENCES users.user(id) ON DELETE CASCADE;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.userbadge 
                ADD CONSTRAINT fk_userBadge_badgeId 
                FOREIGN KEY (badgeid) REFERENCES gaming.badge(id) ON DELETE CASCADE;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # UserPoint foreign keys
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.userpoint 
                ADD CONSTRAINT fk_userPoint_userId 
                FOREIGN KEY (userid) REFERENCES users.user(id) ON DELETE CASCADE;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # UserAction foreign keys
        cursor.execute("""
            DO $$ BEGIN
                ALTER TABLE gaming.useraction 
                ADD CONSTRAINT fk_userAction_userId 
                FOREIGN KEY (userid) REFERENCES users.user(id) ON DELETE CASCADE;
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)


def reverse_create_gaming_schema(apps, schema_editor):
    """Drop gaming schema (be careful!)"""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA IF EXISTS gaming CASCADE;")


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
        ('roadmap_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_gaming_schema, reverse_create_gaming_schema),
    ]
