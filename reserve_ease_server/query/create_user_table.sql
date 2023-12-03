CREATE TABLE users (
    id UUID PRIMARY KEY, -- UUID型の主キー
    supabase_id UUID NOT NULL, -- Supabaseの認証システムから提供される一意のユーザーID
    first_name VARCHAR(255) NOT NULL, -- 名
    last_name VARCHAR(255) NOT NULL, -- 姓
    email VARCHAR(255) UNIQUE NOT NULL, -- メールアドレス
    phone_number VARCHAR(255), -- 電話番号
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- 作成日時
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- 更新日時
);

ALTER TABLE users
ALTER COLUMN id SET DEFAULT uuid_generate_v4();

ALTER TABLE users
ADD CONSTRAINT unique_supabase_id UNIQUE (supabase_id);
