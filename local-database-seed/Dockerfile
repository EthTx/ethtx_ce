FROM mongo

COPY addresses.json /addresses.json
COPY contracts.json /contracts.json
COPY seed.sh /seed.sh

CMD ["sh", "seed.sh"]