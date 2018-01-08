-- ### sentences
create table sentences (
    sentence_id serial primary key,
    sentence varchar(255) not null,
    channel varchar(255) not null,
    create_date timestamp default CURRENT_TIMESTAMP,/*作成日時*/
    update_date timestamp default CURRENT_TIMESTAMP/*更新日時*/
);

-- ### words
/*表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音*/
create table words (
    word_id serial primary key,
    word varchar(255) not null, /*表層形*/
    part_of_speech varchar(255) default '*', /*品詞*/
    part_of_speech_detail1 varchar(255) default '*', /*品詞細分類1*/
    part_of_speech_detail2 varchar(255) default '*', /*品詞細分類2*/
    part_of_speech_detail3 varchar(255) default '*', /*品詞細分類3*/
    conjugate1 varchar(255) default '*', /*活用型*/
    conjugate2 varchar(255) default '*', /*活用形*/
    original varchar(255) default '*', /*原形*/
    pronunciation1 varchar(255) default '*', /*読み*/
    pronunciation2 varchar(255) default '*', /*発音*/
    create_date timestamp default CURRENT_TIMESTAMP,/*作成日時*/
    update_date timestamp default CURRENT_TIMESTAMP/*更新日時*/
);

-- ### sentence_word
create table sentence_word (
    sentence_word_id serial primary key,
    sentence_id int not null,
    word_id int not null,
    channel varchar(255) not null,
    create_date timestamp default CURRENT_TIMESTAMP,/*作成日時*/
    update_date timestamp default CURRENT_TIMESTAMP/*更新日時*/
);

-- ### markov_chain
-- マルコフ連鎖を3単語で行うためのテーブル

create table markov_chain (
    markov_chain_id serial primary key,
    word1 varchar(255) not null,
    word2 varchar(255) not null,
    word3 varchar(255) not null,
    channel varchar(255) not null,
    create_date timestamp default CURRENT_TIMESTAMP,/*作成日時*/
    update_date timestamp default CURRENT_TIMESTAMP/*更新日時*/
);

-- 検索用にindexを生成
create index word2_index on markov_chain(word2, channel);
