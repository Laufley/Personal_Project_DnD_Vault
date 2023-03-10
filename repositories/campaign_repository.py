from db.run_sql import run_sql

from models.player import Player
from models.campaign import Campaign
import repositories.player_repository as player_repository



def delete_all():
    sql = "DELETE FROM campaigns"
    run_sql(sql)
    
def delete(id):
    sql = "DELETE FROM campaigns WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def save(campaign):
    sql = "INSERT INTO campaigns (title, genre, dm, max_capacity, price, details, picture_url) VALUES ( %s, %s, %s, %s, %s, %s, %s) RETURNING *"
    values = [campaign.title, campaign.genre, campaign.dm, campaign.max_capacity, campaign.price, campaign.details, campaign.picture_url]
    results = run_sql( sql, values )
    campaign.id = results[0]['id']
    return campaign


def select_all_campaigns():
    list_of_campaigns = []
    
    sql = "SELECT * FROM campaigns"
    results = run_sql(sql)
    for row in results:
        campaign = Campaign(row['title'], row['genre'], row['dm'], row['max_capacity'], row['price'], row['details'], row['picture_url'], row['id'],)
        list_of_campaigns.append(campaign)
    return list_of_campaigns


def select(id):
    campaign = None
    sql = "SELECT * FROM campaigns WHERE id = %s"
    values = [id]
    results = run_sql(sql, values)
    
    if results:
        found = results[0]
        campaign = Campaign(found['title'], found['genre'], found['dm'], found['max_capacity'], found['price'], found['details'], found['picture_url'], found['id'],)
    return campaign

def update(campaign):
    sql = "UPDATE campaigns SET (title, genre, dm, max_capacity, price, details, picture_url) = (%s, %s, %s, %s, %s, %s, %s) WHERE id = %s"
    values = [campaign.title, campaign.genre, campaign.dm, campaign.max_capacity, campaign.price, campaign.details, campaign.picture_url, campaign.id]
    run_sql(sql, values)
    

def campaigns_per_player(player_id):
    missions = []

    sql = "SELECT campaigns.* FROM campaigns INNER JOIN players_history ON players_history.campaign_id = campaigns.id WHERE player_id = %s"
    values = [player_id]
    results = run_sql(sql, values)

    for row in results:
        mission = Campaign(row['title'], row['genre'], row['dm'], row['max_capacity'], row['price'], row['details'], row['picture_url'])
        missions.append(mission)

    return missions