"""Recover only verifiable metadata for the known Aug1 GEN-DK corrupt map.
Never invent the unavailable numeric telemetry, or reuse the wrong GOL game.
"""
import copy,json,urllib.request
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'results/s16_jul_oct';RAW=R/'data/raw/detailed/s16_jul_oct'
ID='115548147900553473';GAME='115548147900553474'
def main():
    p=D/'series.json';data=json.loads(p.read_text());record=next(r for r in data if r['official']['id']==ID)
    if record.get('resolution'):print('Existing explicit metadata resolution retained');return
    assert record['status']=='map_score_conflict'
    (D/'conflicts').mkdir(exist_ok=True);(D/'conflicts'/(ID+'_original.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    metadata_path=RAW/'riot_gen_dk_game1_window.json'
    if not metadata_path.exists():
        RAW.mkdir(parents=True,exist_ok=True)
        metadata_path.write_bytes(urllib.request.urlopen('https://feed.lolesports.com/livestats/v1/window/'+GAME,timeout=30).read())
    response=json.loads(metadata_path.read_text());assert response['esportsGameId']==GAME and response['esportsMatchId']==ID
    meta=response['gameMetadata'];game=next(g for g in record['games'] if g['game']==1);original_fields=list(game['teams']['blue']['players'][0]['stats'])
    names={'GEN':'Gen.G Esports','DK':'Dplus KIA'};roles={'top':'TOP','jungle':'JUNGLE','mid':'MID','bottom':'ADC','support':'SUPPORT'};teams={}
    official=record['official'];assert (official['team1'],official['wins1'],official['team2'],official['wins2'])==('Gen.G Esports',0,'Dplus KIA',2)
    for side in ('blue','red'):
        roster=meta[side+'TeamMetadata']['participantMetadata'];prefixes={p['summonerName'].split(' ',1)[0] for p in roster};assert len(prefixes)==1
        name=names[prefixes.pop()];players=[]
        for player in roster:
            players.append(dict(name=player['summonerName'].split(' ',1)[1],role=roles[player['role']],champion_asset=player['championId'],esports_player_id=player['esportsPlayerId'],stats={k:'' for k in original_fields}))
        assert len(players)==5
        teams[side]=dict(name=name,win=int(name=='Dplus KIA'),players=players,total_gold=None,gold_difference_15=None,cs=None,kills=None)
    official_url='https://lolesports.com/en-US/vod/'+ID+'/1';feed_url='https://feed.lolesports.com/livestats/v1/window/'+GAME
    game.update(teams=teams,patch='.'.join(meta['patchVersion'].split('.')[:2]),duration=None,esports_game_id=GAME,sources=[official_url,feed_url],numeric_stats_status='unavailable: official feed returned all-zero placeholders; GOL map is inconsistent',metadata_status='verified from official match/game identifiers and ten-player metadata',winner_provenance='Both map winners follow uniquely from official 0-2 series score')
    record.update(status='verified',resolution=dict(type='official_metadata_only',game=1,description='Replace corrupt GOL map1 labels/roster/champions using official game metadata. Numeric telemetry and duration are missing, never imputed. Official 0-2 determines both winners.',official_sources=[official_url,feed_url],raw_metadata=str((RAW/'riot_gen_dk_game1_window.json').relative_to(R))),resolved_map_score={'Gen.G Esports':0,'Dplus KIA':2})
    # This normalized record can be reused by a resumed collection without
    # silently reverting to the known corrupt GOL result. Original stays above.
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');work=R/'.local/s16_jul_oct/series'/(ID+'.json');work.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    (D/'conflicts'/'resolution.json').write_text(json.dumps(record['resolution'],ensure_ascii=False,indent=2)+'\n')
    print('Recovered official Game1 roster/sides/champions/patch and unambiguous winner; numeric telemetry remains missing')
if __name__=='__main__':main()
