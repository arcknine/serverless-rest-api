### Run DynamoDB locally:

`sls dynamodb start`

### Invoke functions locally:

```
sls invoke local -f create --profile=spuul-dev --data '{"application_id": "1", "section_id": "1", "listing_type": "V2::Pick", "listing_id": "1", "some_attr_1": "a", "some_attr_2": "b"}'
sls invoke local -f create --profile=spuul-dev --data '{"application_id": "1", "section_id": "1", "listing_type": "V2::Pick", "listing_id": "2", "some_attr_1": "c", "some_attr_2": "d"}'

sls invoke local -f get --profile=spuul-dev --data '{"application_id": "1", "section_id": "1", "listing_type": "V2::Pick", "listing_id": "1"}'
sls invoke local -f index --profile=spuul-dev --data '{"application_id": "1", "section_id": "1" }'
sls invoke local -f delete --profile=spuul-dev --data '{"application_id": "1", "section_id": "1", "listing_type": "V2::Pick", "listing_id": "1"}'
```
