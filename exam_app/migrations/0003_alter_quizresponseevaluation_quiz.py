# Generated migration for changing QuizResponseEvaluation to connect to Quiz instead of QuizResponse

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0002_alter_evaluation_table_alter_question_table_and_more'),
    ]

    operations = [
        # Note: Since models are unmanaged (managed=False), 
        # the actual database schema changes need to be done manually via SQL:
        # 
        # ALTER TABLE exam.quizresponseevaluation 
        # DROP CONSTRAINT IF EXISTS idx_qre_quizRespId,
        # DROP COLUMN IF EXISTS quizresponseid,
        # ADD COLUMN quizid INTEGER REFERENCES exam.quiz(id) ON DELETE CASCADE,
        # ADD INDEX idx_qre_quizId (quizid);
        #
        # The score field should store percentage values (already FloatField, no change needed)
        
        migrations.RunSQL(
            sql="""
                -- Drop old foreign key constraint and index
                DROP INDEX IF EXISTS exam.idx_qre_quizRespId;
                
                -- Drop old column
                ALTER TABLE exam.quizresponseevaluation 
                DROP COLUMN IF EXISTS quizresponseid;
                
                -- Add new column
                ALTER TABLE exam.quizresponseevaluation 
                ADD COLUMN IF NOT EXISTS quizid INTEGER;
                
                -- Add foreign key constraint
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'quizresponseevaluation_quizid_fkey'
                    ) THEN
                        ALTER TABLE exam.quizresponseevaluation 
                        ADD CONSTRAINT quizresponseevaluation_quizid_fkey 
                        FOREIGN KEY (quizid) REFERENCES exam.quiz(id) ON DELETE CASCADE;
                    END IF;
                END $$;
                
                -- Create new index
                CREATE INDEX IF NOT EXISTS idx_qre_quizId ON exam.quizresponseevaluation(quizid);
            """,
            reverse_sql="""
                -- Reverse migration: restore old structure
                DROP INDEX IF EXISTS exam.idx_qre_quizId;
                
                ALTER TABLE exam.quizresponseevaluation 
                DROP CONSTRAINT IF EXISTS quizresponseevaluation_quizid_fkey,
                DROP COLUMN IF EXISTS quizid;
                
                ALTER TABLE exam.quizresponseevaluation 
                ADD COLUMN IF NOT EXISTS quizresponseid INTEGER;
                
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'quizresponseevaluation_quizresponseid_fkey'
                    ) THEN
                        ALTER TABLE exam.quizresponseevaluation 
                        ADD CONSTRAINT quizresponseevaluation_quizresponseid_fkey 
                        FOREIGN KEY (quizresponseid) REFERENCES exam.quizresponse(id) ON DELETE CASCADE;
                    END IF;
                END $$;
                
                CREATE INDEX IF NOT EXISTS idx_qre_quizRespId ON exam.quizresponseevaluation(quizresponseid);
            """
        ),
    ]

